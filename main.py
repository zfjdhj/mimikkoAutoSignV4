import os
import re
import sys
import time
import yaml
import grpc
import hashlib
import platform
from apscheduler.schedulers.blocking import BlockingScheduler
from types import SimpleNamespace

from util.logger import Logger
from util.openstick_led import red_on

import proto.activitynew_pb2 as activitynew_pb2
import proto.activitynew_pb2_grpc as activitynew_pb2_grpc
import proto.auth_pb2 as auth_pb2
import proto.auth_pb2_grpc as auth_pb2_grpc
import proto.character_pb2 as character_pb2
import proto.character_pb2_grpc as character_pb2_grpc
import proto.energy_pb2 as energy_pb2
import proto.energy_pb2_grpc as energy_pb2_grpc
import proto.mail_pb2 as mail_pb2
import proto.mail_pb2_grpc as mail_pb2_grpc
import proto.material_pb2 as material_pb2
import proto.material_pb2_grpc as material_pb2_grpc
import proto.param_pb2 as param_pb2
import proto.sign_pb2 as sign_pb2
import proto.sign_pb2_grpc as sign_pb2_grpc
import proto.signin_pb2 as signin_pb2
import proto.signin_pb2_grpc as signin_pb2_grpc
import proto.scalar_pb2 as scalar_pb2
import proto.scalar_pb2_grpc as scalar_pb2_grpc
import proto.store_pb2 as store_pb2
import proto.store_pb2_grpc as store_pb2_grpc
import proto.task_pb2 as task_pb2
import proto.task_pb2_grpc as task_pb2_grpc
import proto.travelv2_pb2 as travelv2_pb2
import proto.travelv2_pb2_grpc as travelv2_pb2_grpc
import proto.work_pb2 as work_pb2
import proto.work_pb2_grpc as work_pb2_grpc

from task.task_travel import task_travel
from task.task_coin_mall import task_coin_mall
from task.task_energy_center import task_energy_center
from task.task_energy_exchange import task_energy_exchange
from task.task_mail_receive import task_mail_receive
from task.task_ordinary_work import task_ordinary_work
from task.task_sign import task_sign
from task.task_task import task_task
from task.task_activity_sign import task_activity_sign
from task.task_update_character_json import task_update_character_json


base_path = os.path.dirname(os.path.abspath(__file__))

# 启动参数设置
if len(sys.argv) == 3:
    device_id = sys.argv[1]
    authorization = sys.argv[2]
else:
    device_id = ""
    authorization = ""


class Client():
    def __init__(self, device_id='', authorization=''):
        self.cfg_file = 'config.yaml'
        self.host = 'api4.mimikko.cn'
        self.port = '443'
        self.agent = "okhttp/5.0.0-alpha.11"
        self.sdkversion = "4"
        self.is_login = True
        # 读取ssl证书
        with open('api4_mimikko_cn.cer', 'rb') as f:
            trusted_certs = f.read()
        credentials = grpc.ssl_channel_credentials(
            root_certificates=trusted_certs)
        # 设置最大消息接收长度16M
        # https://grpc.github.io/grpc/core/group__grpc__arg__keys.html
        MAX_MESSAGE_LENGTH = 16 * 1024 * 1024
        MAX_METADATA_LENGTH = 16 * 1024
        self.ssl_channel = grpc.secure_channel(
            target=self.host + ':' + self.port,
            credentials=credentials,
            options=(
                ('grpc.primary_user_agent', self.agent),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_metadata_size', MAX_METADATA_LENGTH)
            )
        )
        self.load_config()
        self.mimikko_version = self.basic.mimikko_version
        self.delay = self.basic.delay
        if device_id and authorization:
            self.authorization = authorization
            self.device_id = device_id
        elif self.basic.authorization and self.basic.device_id:
            self.authorization = self.basic.authorization
            self.device_id = self.basic.device_id
        elif not self.basic.authorization and self.basic.device_id:
            self.log.warning("缺少账户信息,authorization,但是有device_id，满足自动登录")
            self.authorization = "Bearer"
            self.device_id = self.basic.device_id
            self.is_login = self.login()
        else:
            self.log.error("缺少账户信息,device_id authorization")
            sys.exit(0)

    def load_config(self,):
        with open(self.cfg_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.basic = SimpleNamespace(**config['Basic'])
        self.task = SimpleNamespace(**config['Task'])
        if self.basic.debug:
            self.log = Logger(
                base_path,
                base_path + "/log/main.log",
                level="debug").logger
        else:
            self.log = Logger(
                base_path,
                base_path + "/log/main.log",
                level="info",
                sfmt="[%(asctime)s][%(levelname)s]:%(message)s").logger

    def login(self,):
        if self.basic.account:
            self.log.warning("登录状态出错，即将重新登录获取authorization")
            account = self.basic.account
            password = self.basic.password
            password_hash = hashlib.sha256(
                bytes(password, encoding='utf8')).hexdigest()
            res = self.call_api("Auth/Login", accountType=3,
                                account=account, password=password_hash)
            if res.token:
                self.authorization = f"Bearer {res.token}"
                for i in range(len(self.metadata)):
                    if self.metadata[i][0] == 'authorization':
                        self.metadata[i] = (
                            'authorization', self.authorization)
                        break
                self.logwarning("更新config文件,原文件已备份config_old.yaml")
                with open(self.cfg_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    with open('config_old.yaml', 'w',
                              encoding='utf-8') as f_old:
                        f_old.write(content)
                with open(self.cfg_file, 'r+', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    config["Basic"]["authorization"] = self.authorization
                with open(self.cfg_file, 'w+', encoding='utf-8') as f:
                    yaml.dump(config, f,
                              sort_keys=False,
                              encoding='utf-8',
                              allow_unicode=True)
                self.log.warning(f"new authorization:{res.token}")
                self.is_login = True
            else:
                self.log.error("登录出错，将在下次任务执行时继续尝试登录")
                self.is_login = False
            return self.is_login

    def call_api(self, api_url, content_type='application/grpc', **kw):
        url_list = api_url.split('/')
        package_name = url_list[0].lower()
        pb2_ = globals()[f'{package_name}_pb2']
        grpc_ = globals()[f'{package_name}_pb2_grpc']
        stub = grpc_.__dict__[f'{url_list[0]}Stub']
        sub = stub(channel=self.ssl_channel)
        if kw.get("body"):
            body = kw["body"]
            kw['body'] = pb2_.__dict__[f'{url_list[1]}RequestBody'](**body)
        request = f'{url_list[1]}Request'
        time.sleep(self.delay)
        self.metadata = [('authorization', self.authorization),
                         ('device-id', self.device_id),
                         ('x-mimikko-version-number', self.mimikko_version),
                         ('sdkversion', self.sdkversion),
                         ('user-agent', self.agent),
                         ("te", "trailers"),
                         ('content-type', content_type)]
        res = ''
        try:
            res = sub.__dict__[url_list[1]](
                pb2_.__dict__[request](**kw),
                compression=grpc.Compression.Gzip,
                metadata=self.metadata)
            return res
        except grpc.RpcError as e:
            self.log.error(
                f"call_api error: code={e.code()} message={e.details()}")
            login_text = ["阁下您已在别处登录啦>_<", "请勿重复点击登录按钮", "登录状态失效了( ͡• ͜ʖ ͡• )"]
            if e.details() in login_text:
                if self.login():
                    res = sub.__dict__[url_list[1]](
                        pb2_.__dict__[request](**kw),
                        compression=grpc.Compression.Gzip,
                        metadata=self.metadata)
                    return res
            elif e.details() == "Stream removed":
                self.log.debug("连接失败,重试中...")
                res = sub.__dict__[url_list[1]](
                    pb2_.__dict__[request](**kw),
                    compression=grpc.Compression.Gzip,
                    metadata=self.metadata)
                return res


def camel_to_snake(camel):
    underscore = re.sub('([A-Z])', r'_\1', camel).lower()
    return underscore[1:] if underscore.startswith("_") else underscore


def task_start(device_id="", authorization="", client=""):
    client = Client(device_id, authorization)
    log = client.log
    log.info("脚本执行中....")
    for task_name in client.task.__dict__:
        if client.task.__dict__[task_name]['enable']:
            task = globals()['task_' + camel_to_snake(task_name)]
            try:
                res = task(client)
                if res in globals():
                    client = Client(device_id, authorization)
                    globals()[res](client=client)
            except Exception as e:
                log.error(f"{task_name}:{e}")
                err_openstick(log)
    log.info("脚本执行结束....")


def err_openstick(log):
    os_name = platform.platform()
    if os_name == "Linux-5.15.0-handsomekernel+-aarch64-with-glibc2.29":
        log.info("Openstick系统，红灯亮起")
        red_on()


def main(device_id, authorization):
    client = Client(device_id, authorization)
    log = client.log
    task_start(device_id, authorization)
    if client.basic.scheduler_mode:
        log.info("脚本定时循环启动...")
        scheduler = BlockingScheduler()
        interval_hours = client.basic.scheduler_interval
        scheduler.add_job(
            task_start, 'interval',
            hours=interval_hours,
            args=[device_id, authorization])
        scheduler.start()


if __name__ == '__main__':
    main(device_id, authorization)
