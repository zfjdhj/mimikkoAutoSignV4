import os
import sys
import time
import yaml
import grpc

from types import SimpleNamespace
from util.logger import Logger
import proto.sign_pb2 as sign_pb2
import proto.sign_pb2_grpc as sign_pb2_grpc
import proto.character_pb2 as character_pb2
import proto.character_pb2_grpc as character_pb2_grpc


base_path = os.path.dirname(os.path.abspath(__file__))
if base_path == "":
    base_path = "/home/runner/work/mimikkoAutoSignIn/mimikkoAutoSignIn"
    os.system(f"chmod 777 {base_path}")

# log信息配置
if not os.path.exists(base_path + "/log"):
    os.makedirs(f"{base_path}/log", mode=777)
    os.system(f"chmod 777 {base_path}/log")
date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
log = Logger(base_path, base_path + f"/log/{date}.log", level="debug").logger
# log.info("test")

# 启动参数设置
if len(sys.argv) == 3:
    device_id = sys.argv[1]
    authorization = sys.argv[2]
else:
    device_id = ""
    authorization = ""


class Client():
    def __init__(self, device_id, authorization):
        self.cfg_file = 'config.yaml'
        self.host = 'api4.mimikko.cn'
        self.port = '443'
        self.agent = "okhttp/5.0.0-alpha.11"
        self.mimikko_version = "40002"
        self.sdkversion = "4"
        self.agent = "okhttp/5.0.0-alpha.11"
        self.load_config(device_id, authorization)
        self.metadata = ((('authorization', self.authorization),
                          ('device-id', self.device_id),
                          ('x-mimikko-version-number', self.mimikko_version),
                          ('sdkversion', self.sdkversion),
                          ('user-agent', self.agent),
                          ("te", "trailers")
                          ))
        # 读取ssl证书
        with open('api4_mimikko_cn.cer', 'rb') as f:
            trusted_certs = f.read()
        credentials = grpc.ssl_channel_credentials(
            root_certificates=trusted_certs)
        self.ssl_channel = grpc.secure_channel(
            target=self.host + ':' + self.port,
            credentials=credentials,
            options=(('grpc.primary_user_agent', self.agent),))
        pass

    def load_config(self, device_id, authorization):
        with open(self.cfg_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.basic = SimpleNamespace(**config['Basic'])
        self.task = SimpleNamespace(**config['Task'])
        if device_id and authorization:
            self.authorization = authorization
            self.device_id = device_id
        elif self.basic.authorization and self.basic.device_id:
            self.authorization = self.basic.authorization
            self.device_id = self.basic.device_id
        else:
            log.error("缺少账户信息,device_id authorization")
            sys.exit(0)
        self.delay = self.basic.delay
        pass

    def GetUserSignStatus(self):
        # 查询签到信息
        sub = sign_pb2_grpc.SignStub(channel=self.ssl_channel)
        res = sub.GetUserSignStatus(
            sign_pb2.EMPTY_request(),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def Sign(self):
        # 签到
        sub = sign_pb2_grpc.SignStub(channel=self.ssl_channel)
        res = sub.Sign(
            sign_pb2.request(character="character_miruku2"),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def EnergyExchange(self, character_code):
        # 兑换成长值
        sub = character_pb2_grpc.CharacterStub(channel=self.ssl_channel)
        res = sub.EnergyExchange(
            character_pb2.request(character_code=character_code),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res


def task_sign(client):
    # 任务：每日签到
    res = ""
    log.info("签到任务执行中...")
    time.sleep(client.delay)
    # 1.获取签到信息
    sign_info = client.GetUserSignStatus()
    res = f"当前累计签到{sign_info.continuousSign}天,今日{'已' if sign_info.isSign else '未'}签到"
    log.info(res)
    if not sign_info.isSign:
        # 2.签到
        time.sleep(client.Basic.delay)
        client.Sign()
        log.info("今日还未签到，签到中...")
    return res


def task_energy_exchange(client, character_code):
    # 任务：成长值兑换
    res = ""
    log.info("成长值兑换任务执行中...")
    time.sleep(client.delay)
    client.EnergyExchange(character_code)


def main(device_id, authorization):
    client = Client(device_id, authorization)
    if client.task.Sign["enable"]:
        task_sign(client)
    if client.task.EnergyExchange["enable"]:
        task_energy_exchange(client, client.task.EnergyExchange["character_code"])


if __name__ == '__main__':
    main(device_id, authorization)
