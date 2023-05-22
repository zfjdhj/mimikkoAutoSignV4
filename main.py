import os
import sys
import time
import yaml
import grpc
import hashlib
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED
from types import SimpleNamespace

from util.logger import Logger
import proto.sign_pb2 as sign_pb2
import proto.sign_pb2_grpc as sign_pb2_grpc
import proto.character_pb2 as character_pb2
import proto.character_pb2_grpc as character_pb2_grpc
import proto.scalar_pb2 as scalar_pb2
import proto.scalar_pb2_grpc as scalar_pb2_grpc
import proto.energy_pb2 as energy_pb2
import proto.energy_pb2_grpc as energy_pb2_grpc
import proto.work_pb2 as work_pb2
import proto.work_pb2_grpc as work_pb2_grpc
import proto.task_pb2 as task_pb2
import proto.task_pb2_grpc as task_pb2_grpc
import proto.mail_pb2 as mail_pb2
import proto.mail_pb2_grpc as mail_pb2_grpc
import proto.auth_pb2 as auth_pb2
import proto.auth_pb2_grpc as auth_pb2_grpc
import proto.param_pb2 as param_pb2


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
        self.sdkversion = "4"
        self.is_login = True
        self.load_config(device_id, authorization)
        self.mimikko_version = self.basic.mimikko_version
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
        if self.basic.debug:
            log = Logger(base_path, base_path + f"/log/{date}.log", level="debug").logger
        else:
            log = Logger(base_path, base_path + f"/log/{date}.log", level="info").logger
        if device_id and authorization:
            self.authorization = authorization
            self.device_id = device_id
        elif self.basic.authorization and self.basic.device_id:
            self.authorization = self.basic.authorization
            self.device_id = self.basic.device_id
        elif not self.basic.authorization and self.basic.device_id:
            log.warning("缺少账户信息,authorization,但是有device_id，满足自动登录")
            self.authorization = "Bearer"
            self.device_id = self.basic.device_id
            self.is_login = False
        else:
            log.error("缺少账户信息,device_id authorization")
            sys.exit(0)
        self.delay = self.basic.delay
        pass

    def login(self,):
        if self.basic.account:
            log.warning("登录状态出错，即将重新登录获取authorization")
            account = self.basic.account
            password = self.basic.password
            password_hash = hashlib.sha256(bytes(password, encoding='utf8')).hexdigest()
            res = self.call_api("Auth/Login", accountType=3, account=account, password=password_hash)
            if res.token:
                self.authorization = f"Bearer {res.token}"
                log.warning("更新config文件,原文件已备份config_old.yaml")
                with open(self.cfg_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    with open('config_old.yaml', 'w', encoding='utf-8') as f_old:
                        f_old.write(content)
                with open(self.cfg_file, 'r+', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    config["Basic"]["authorization"] = self.authorization
                with open(self.cfg_file, 'w+', encoding='utf-8') as f:
                    yaml.dump(config, f)
                log.warning(f"new authorization:{res.token}")
                self.is_login = True
            else:
                log.error("登录出错，将在下次任务执行时继续尝试登录")
                self.is_login = False
            return

    def call_api(self, api_url, **kw):
        # api_url='Character/ReceiveCharacterLevelReward'
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
        try:
            res = sub.__dict__[url_list[1]](pb2_.__dict__[request](
                **kw), compression=grpc.Compression.Gzip, metadata=self.metadata)
        except grpc.RpcError as e:
            log.error(f"call_api error: code={e.code()} message={e.details()}")
            login_text = ["阁下您已在别处登录啦>_<", "请勿重复点击登录按钮", "登录状态失效了( ͡• ͜ʖ ͡• )"]
            if e.details() in login_text:
                self.login()
        else:
            if not self.is_login:
                self.is_login = True
            log.debug(grpc.StatusCode.OK)
        # sys.exit(0)
        return res


def task_sign(client, character_code):
    # 任务：每日签到
    if not client.is_login:
        return
    res = ""
    log.info("「签到」任务执行中...")
    # 1.获取签到信息
    sign_info = client.call_api("Sign/GetUserSignStatus")
    log.debug(sign_info)
    res = f"当前累计签到{sign_info.continuousSign}天,今日{'已' if sign_info.todaySign else '未'}签到"
    log.info(res)
    if not sign_info.todaySign:
        # 2.签到
        log.info("今日还未签到，签到中...")
        client.call_api("Sign/Sign", **{"characterCode": character_code})
    return res


def task_energy_exchange(client, character_code):
    # 任务：成长值兑换
    if not client.is_login:
        return
    log.info("「成长值兑换」任务执行中...")
    # # 获取能量值(用于兑换成长值)信息
    res = client.call_api("Scalar/GetUserAutoScalar", **{"code": "user_energy"})
    # print(res)
    if res.newValue > 0:
        character_code = client.task.EnergyExchange['character_code']
        res2 = client.call_api("Character/EnergyExchange", characterCode=character_code)
        if res2.characterCode == character_code:
            log.info(f"{character_code}成长值兑换成功")
            # # 助手升级
            char_info = client.call_api("Character/ListCharacter", page=1, pageSize=60)
            for char in char_info.content:
                if char.existNextLevel:
                    log.debug(f"存在后续等级{char.existNextLevel}")
                    for statistic in char.statistics:
                        if statistic.typeCode == 'character_favour':
                            if statistic.value > statistic.maxValue:
                                log.info(f"{char.name}满足升级条件，升级中....")
                                client.call_api("Character/CharacterLevelManualUpgrade", code=char.code)
                # # 领取助手升级奖励
                if client.task.EnergyExchange["receive_level_reward"]:
                    reward_info = client.call_api("Character/ListCharacterLevelReward",
                                                  code=char.code, page=1, pageSize=60)
                    for reward in reward_info.content:
                        status = character_pb2.CharacterLevelRewardReplyStatus.Name(reward.status)
                        if status == "AVAILABLE":
                            reward_detail = ""
                            for r in reward.rewards:
                                reward_detail += f"{r.name}*{r.num} "
                            log.info(f"{char.name}领取{reward.level}奖励：{reward_detail}")
                            client.call_api("Character/ReceiveCharacterLevelReward",
                                            levelId=reward.levelId, rewardCollectionId=reward.rewardCollectionId)

        else:
            log.info(f"{character_code}成长值兑换失败")


def task_energy_center(client):
    # 任务：能源中心
    if not client.is_login:
        return
    log.info("「能源中心」任务执行中...")
    # # 获取能源中心仓位信息
    for i in range(2):
        log.info("能源中心check...")
        res = client.call_api("Energy/ListEnergySourceRecord", page=1, pageSize=60)
        for i in res.content:
            status = energy_pb2.Status.Name(i.status)
            if status == 'FINISHED':
                # # # 领取
                res2 = client.call_api("Energy/ReceiveEnergySourceReward", id=i.id)
                log.debug(res2)
                log.info(f'能源中心领取{i.position+1}号位')
                continue
            elif status == 'UNLOCKED':
                # # # 创建
                # # # print('获取充能方式-普通芯片-id')
                res3 = client.call_api("Energy/ListEnergySourceModel", page=1, pageSize=60)
                for item in res3.content:
                    if item.name == '普通芯片':
                        # ## 创建充能
                        res4 = client.call_api("Energy/CreateEnergySourceRecord",
                                               modelId=item.modelId, position=i.position)
                        log.debug(res4)
                        log.info(f'能源中心创建充能{i.position+1}号位')
                continue
    else:
        log.info("能源中心暂时没有事情做")


def task_ordinary_work(client):
    # 任务：公会悬赏任务
    if not client.is_login:
        return
    log.info("「公会悬赏」任务执行中...")
    for i in range(2):
        log.info("公会悬赏任务check...")
        work_list = client.call_api("Work/ListOrdinaryWork", page=1, pageSize=60)
        log.debug(f"今日悬赏任务{work_list.total}个")
        for work in work_list.content:
            status = work_pb2.PlayStatus.Name(work.playStatus)
            if status == 'CAN_RECEIVE':
                # # 收取奖励
                # 获取任务详细信息
                work_info = client.call_api("Work/GetOrdinaryWorkRecord", id=work.recordId)
                reward_info = client.call_api("Work/ReceiveOrdinaryWorkReward", id=work.recordId)
                log.info("收取{}级任务{}，奖励:{}*{}".format(
                    work_info.level,
                    work_info.workName,
                    reward_info.rewards.scalarName,
                    reward_info.rewards.value)
                )
            elif status == 'NOT_STARTED':
                character_list = client.call_api("Work/ListWorksCharacter", page=1, pageSize=60)
                log.debug(f"当前空闲助手{character_list.total}个")
                work_characters = client.task.OrdinaryWork["work_characters"]
                for character in character_list.content:
                    if character.code in work_characters:
                        log.info("{}将被派往执行{}级任务{}，奖励:{}*{}".format(
                            character.name,
                            work.level,
                            work.name,
                            work.rewards.scalarName,
                            work.rewards.value
                        ))
                        client.call_api("Work/PickOrdinaryWork",
                                        body={"characterCode": character.code}, id=work.recordId)
                        break
    else:
        log.info("公会悬赏暂时没有事情做")


def task_task(client):
    # 任务：助手每日任务
    if not client.is_login:
        return
    log.info("「助手每日任务」执行中...")
    task_level = ["S", "A", "B", "C", "D"]
    for i in range(len(client.task.Task["task_characters"])):
        log.info("助手任务check...")
        task_list_character = client.call_api("Task/ListTask", type="character", page=1, pageSize=60)
        task_list_daily = client.call_api("Task/ListTask", type="daily", page=1, pageSize=60)
        task_list = [x for x in task_list_character.content] + [x for x in task_list_daily.content]
        for allow in task_level:
            for task in task_list:
                if task.level == allow:
                    status = param_pb2.PlayStatus.Name(task.status)
                    if status == 'CAN_RECEIVE':
                        # # 收取奖励
                        # 获取任务详细信息
                        task_info = client.call_api("Task/GetTaskRecord", id=task.recordId)
                        reward_info = client.call_api("Task/ReceiveTaskReward", id=task.recordId)
                        log.info("收取{}级任务{}，奖励:{}*{}".format(
                            task_info.level,
                            task_info.name,
                            reward_info.rewards.scalarName,
                            reward_info.rewards.value)
                        )
                        break
                    elif status == "NOT_STARTED":
                        task_info = client.call_api("Task/GetTaskRecord", id=task.recordId)
                        character_list = client.call_api(
                            "Task/ListTaskCharacter", id=task_info.id, page=1, pageSize=60)
                        log.debug(f"{task.level}级任务，当前可参与空闲助手{character_list.total}个")
                        task_characters = client.task.Task["task_characters"]
                        for character in character_list.content:
                            if character.code in task_characters:
                                log.info("{}将去参与{}级任务：{}，奖励:{}*{}".format(
                                    character.name,
                                    task_info.level,
                                    task_info.name,
                                    task_info.characterRewards.rewards.scalarName,
                                    task_info.characterRewards.rewards.value
                                ))
                                pick_info = client.call_api(
                                    "Task/PickTask", id=task_info.recordId, body={"characterCode": character.code})
                                log.info(f"参与成功,{pick_info.value}")
                                break
                        continue
            else:
                continue
            break
    else:
        log.info("助手任务暂时没有事情做")


def task_mail_receive(client):
    # 任务：邮件一键领取
    if not client.is_login:
        return
    log.info("「邮件一键领取」任务执行中...")
    # # 获取邮件列表
    mail_list = client.call_api("Mail/ListMail", page=1, pageSize=60)
    for mail in mail_list.content:
        if not mail.received:
            res = client.call_api("Mail/ReceiveAllMailAttachment")
            for reward in res.contents:
                log.info(f"邮件奖励获得：{reward.name}*{reward.num}")
            break
    else:
        log.info("邮件领取暂时没有事情做")


def task_coin_mall(client):
    # 任务：硬币商店
    if not client.is_login:
        return
    log.info("「硬币商店」任务执行中...")
    # # 获取商店物品列表
    exchange_list = client.call_api("Scalar/ListCoinExchangeRelation", page=1, pageSize=60)
    for exchange in exchange_list.content:
        if exchange.target.materialCode in client.task.CoinMall['exchange_list']:
            times = exchange.maxTimes - exchange.userTimes
            log.debug(f"本周还可换取{times}次{exchange.target.materialName}")
            if exchange.maxTimes > exchange.userTimes:
                # # 兑换
                relation_code = exchange.relationCode
                relation_type = exchange.relationType
                log.info(f"硬币换取{times}次{exchange.target.materialName}")
                client.call_api("Scalar/Exchange",
                                relationCode=relation_code,
                                relationType=relation_type,
                                times=times
                                )


def task_start(device_id, authorization):
    log.info("脚本执行中....")
    client = Client(device_id, authorization)
    if client.is_login:
        if client.task.Sign["enable"]:
            task_sign(client, client.task.EnergyExchange["character_code"])
        if client.task.EnergyExchange["enable"]:
            task_energy_exchange(client, client.task.EnergyExchange["character_code"])
        if client.task.EnergyCenter["enable"]:
            task_energy_center(client)
        if client.task.OrdinaryWork["enable"]:
            task_ordinary_work(client)
        if client.task.Task["enable"]:
            task_task(client)
        if client.task.MailReceive["enable"]:
            task_mail_receive(client)
        if client.task.CoinMall["enable"]:
            task_coin_mall(client)
        log.info("脚本执行结束....")
    else:
        log.info("登录中....")
        client.login()
        if client.is_login:
            task_start(device_id, authorization)


def job_execute(event):
    """
    监听事件处理
    :param event:
    :return:
    """
    log.info("脚本循环执行一次结束...")


def main(device_id, authorization):
    client = Client(device_id, authorization)
    task_start(device_id, authorization)
    if client.basic.scheduler_mode:
        log.info("脚本定时循环启动...")
        scheduler = BlockingScheduler()
        interval_hours = client.basic.scheduler_interval
        scheduler.add_job(task_start, 'interval', hours=interval_hours, args=[device_id, authorization])
        scheduler.add_listener(job_execute, EVENT_JOB_EXECUTED)
        scheduler.start()


if __name__ == '__main__':
    main(device_id, authorization)
