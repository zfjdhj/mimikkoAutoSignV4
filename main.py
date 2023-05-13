import os
import sys
import time
import yaml
import grpc
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
        else:
            log.error("缺少账户信息,device_id authorization")
            sys.exit(0)
        self.delay = self.basic.delay
        pass

    def GetUserSignStatus(self):
        # 查询签到信息
        time.sleep(self.delay)
        sub = sign_pb2_grpc.SignStub(channel=self.ssl_channel)
        res = sub.GetUserSignStatus(
            sign_pb2.EMPTY_request(),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def Sign(self, character_code):
        # 签到
        time.sleep(self.delay)
        sub = sign_pb2_grpc.SignStub(channel=self.ssl_channel)
        res = sub.Sign(
            sign_pb2.request(characterCode=character_code),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def GetUserAutoScalar(self):
        # 获取能量值信息
        time.sleep(self.delay)
        sub = scalar_pb2_grpc.ScalarStub(channel=self.ssl_channel)
        res = sub.GetUserAutoScalar(
            scalar_pb2.request(code="user_energy"),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def EnergyExchange(self, character_code):
        # 兑换成长值
        time.sleep(self.delay)
        sub = character_pb2_grpc.CharacterStub(channel=self.ssl_channel)
        res = sub.EnergyExchange(
            character_pb2.request(character_code=character_code),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListEnergySourceRecord(self,):
        time.sleep(self.delay)
        sub = energy_pb2_grpc.EnergyStub(channel=self.ssl_channel)
        res = sub.ListEnergySourceRecord(
            energy_pb2.request2(page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ReceiveEnergySourceReward(self, id: int):
        time.sleep(self.delay)
        sub = energy_pb2_grpc.EnergyStub(channel=self.ssl_channel)
        res = sub.ReceiveEnergySourceReward(
            energy_pb2.request4(id=id),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListEnergySourceModel(self):
        time.sleep(self.delay)
        sub = energy_pb2_grpc.EnergyStub(channel=self.ssl_channel)
        res = sub.ListEnergySourceModel(
            energy_pb2.request(page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def CreateEnergySourceRecord(self, model_id: int, position):
        time.sleep(self.delay)
        sub = energy_pb2_grpc.EnergyStub(channel=self.ssl_channel)
        res = sub.CreateEnergySourceRecord(
            energy_pb2.request3(modelId=model_id, position=position),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListOrdinaryWork(self):
        time.sleep(self.delay)
        sub = work_pb2_grpc.WorkStub(channel=self.ssl_channel)
        res = sub.ListOrdinaryWork(
            work_pb2.request(page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def GetOrdinaryWorkRecord(self, id):
        time.sleep(self.delay)
        sub = work_pb2_grpc.WorkStub(channel=self.ssl_channel)
        res = sub.GetOrdinaryWorkRecord(
            work_pb2.request2(id=id),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ReceiveOrdinaryWorkReward(self, id):
        time.sleep(self.delay)
        sub = work_pb2_grpc.WorkStub(channel=self.ssl_channel)
        res = sub.ReceiveOrdinaryWorkReward(
            work_pb2.request3(id=id),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListWorksCharacter(self):
        time.sleep(self.delay)
        sub = work_pb2_grpc.WorkStub(channel=self.ssl_channel)
        res = sub.ListWorksCharacter(
            work_pb2.request4(page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def PickOrdinaryWork(self, id, character_code):
        time.sleep(self.delay)
        sub = work_pb2_grpc.WorkStub(channel=self.ssl_channel)
        body = work_pb2.PickOrdinaryWorkRequestBody(characterCode=character_code)
        res = sub.PickOrdinaryWork(
            work_pb2.request5(id=id, body=body),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListTask(self, type):
        time.sleep(self.delay)
        sub = task_pb2_grpc.TaskStub(channel=self.ssl_channel)
        res = sub.ListTask(
            task_pb2.request(type=type, page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def GetTaskRecord(self, record_id):
        time.sleep(self.delay)
        sub = task_pb2_grpc.TaskStub(channel=self.ssl_channel)
        res = sub.GetTaskRecord(
            task_pb2.request2(id=record_id),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        # print(type(res))
        return res

    def ListTaskCharacter(self, id):
        time.sleep(self.delay)
        sub = task_pb2_grpc.TaskStub(channel=self.ssl_channel)
        res = sub.ListTaskCharacter(
            task_pb2.request3(id=id, page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ReceiveTaskReward(self, id):
        time.sleep(self.delay)
        sub = task_pb2_grpc.TaskStub(channel=self.ssl_channel)
        res = sub.ReceiveTaskReward(
            task_pb2.request4(id=id),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def PickTask(self, id, character_code):
        time.sleep(self.delay)
        sub = task_pb2_grpc.TaskStub(channel=self.ssl_channel)
        body = task_pb2.PickTaskRequestBody(characterCode=character_code)
        res = sub.PickTask(
            task_pb2.request5(id=id, body=body),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListMail(self):
        time.sleep(self.delay)
        sub = mail_pb2_grpc.MailStub(channel=self.ssl_channel)
        res = sub.ListMail(
            mail_pb2.request(page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ReceiveAllMailAttachment(self):
        time.sleep(self.delay)
        sub = mail_pb2_grpc.MailStub(channel=self.ssl_channel)
        res = sub.ReceiveAllMailAttachment(
            mail_pb2.request3(),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListCoinExchangeRelation(self):
        time.sleep(self.delay)
        sub = scalar_pb2_grpc.ScalarStub(channel=self.ssl_channel)
        res = sub.ListCoinExchangeRelation(
            scalar_pb2.request3(page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def Exchange(self, relation_code, relation_type, times):
        time.sleep(self.delay)
        sub = scalar_pb2_grpc.ScalarStub(channel=self.ssl_channel)
        res = sub.Exchange(
            scalar_pb2.request4(
                relationCode=relation_code,
                relationType=relation_type,
                times=times),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListCharacter(self,):
        time.sleep(self.delay)
        sub = character_pb2_grpc.CharacterStub(channel=self.ssl_channel)
        res = sub.ListCharacter(
            character_pb2.request2(
                page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def CharacterLevelManualUpgrade(self, character_code):
        time.sleep(self.delay)
        sub = character_pb2_grpc.CharacterStub(channel=self.ssl_channel)
        res = sub.CharacterLevelManualUpgrade(
            character_pb2.request3(
                code=character_code),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ListCharacterLevelReward(self, character_code):
        time.sleep(self.delay)
        sub = character_pb2_grpc.CharacterStub(channel=self.ssl_channel)
        res = sub.ListCharacterLevelReward(
            character_pb2.request4(
                code=character_code, page=1, pageSize=60),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res

    def ReceiveCharacterLevelReward(self, level_id, reward_collection_id):
        time.sleep(self.delay)
        sub = character_pb2_grpc.CharacterStub(channel=self.ssl_channel)
        res = sub.ReceiveCharacterLevelReward(
            character_pb2.request5(levelId=level_id, rewardCollectionId=reward_collection_id),
            compression=grpc.Compression.Gzip,
            metadata=self.metadata)
        return res


def task_sign(client, character_code):
    # 任务：每日签到
    res = ""
    log.info("「签到」任务执行中...")
    # 1.获取签到信息
    sign_info = client.GetUserSignStatus()
    log.debug(sign_info)
    res = f"当前累计签到{sign_info.continuousSign}天,今日{'已' if sign_info.todaySign else '未'}签到"
    log.info(res)
    if not sign_info.todaySign:
        # 2.签到
        log.info("今日还未签到，签到中...")
        client.Sign(character_code=character_code)
    return res


def task_energy_exchange(client, character_code):
    # 任务：成长值兑换
    log.info("「成长值兑换」任务执行中...")
    # # 获取能量值(用于兑换成长值)信息
    res = client.GetUserAutoScalar()
    # print(res)
    if res.newValue > 0:
        # character_code = "character_miruku2"
        character_code = client.task.EnergyExchange['character_code']
        res2 = client.EnergyExchange(character_code)
        if res2.character_code == character_code:
            log.info(f"{character_code}成长值兑换成功")
            # # 助手升级
            char_info = client.ListCharacter()
            for char in char_info.content:
                if char.existNextLevel:
                    log.debug(f"存在后续等级{char.existNextLevel}")
                    for statistic in char.statistics:
                        if statistic.typeCode == 'character_favour':
                            if statistic.value > statistic.maxValue:
                                log.info(f"{char.name}满足升级条件，升级中....")
                                client.CharacterLevelManualUpgrade(character_code=char.code)
                                break
                # # 领取助手升级奖励
                if client.task.EnergyExchange["receive_level_reward"]:
                    reward_info = client.ListCharacterLevelReward(character_code=char.code)
                    for reward in reward_info.content:
                        status = character_pb2.CharacterLevelRewardReplyStatus.Name(reward.status)
                        if status == "AVAILABLE":
                            reward_detail = ""
                            for r in reward.rewards:
                                reward_detail += f"{r.name}*{r.num} "
                            log.info(f"{char.name}领取{reward.level}奖励：{reward_detail}")
                            client.ReceiveCharacterLevelReward(
                                level_id=reward.levelId, reward_collection_id=reward.rewardCollectionId)

        else:
            print(f"{character_code}成长值兑换失败")


def task_energy_center(client):
    # 任务：能源中心
    log.info("「能源中心」任务执行中...")
    # # 获取能源中心仓位信息
    for i in range(2):
        log.info("能源中心check...")
        res = client.ListEnergySourceRecord()
        for i in res.content:
            status = energy_pb2.Status.Name(i.status)
            if status == 'FINISHED':
                # # # 领取
                res2 = client.ReceiveEnergySourceReward(i.id)
                log.debug(res2)
                log.info(f'能源中心领取{i.position+1}号位')
                continue
            elif status == 'UNLOCKED':
                # # # 创建
                # # # print('获取充能方式-普通芯片-id')
                res3 = client.ListEnergySourceModel()
                for item in res3.content:
                    if item.name == '普通芯片':
                        # ## 创建充能
                        res4 = client.CreateEnergySourceRecord(model_id=item.modelId, position=i.position)
                        log.debug(res4)
                        log.info(f'能源中心创建充能{i.position+1}号位')
                continue
    else:
        log.info("能源中心暂时没有事情做")


def task_ordinary_work(client):
    # 任务：公会悬赏任务
    log.info("「公会悬赏」任务执行中...")
    for i in range(2):
        log.info("公会悬赏任务check...")
        work_list = client.ListOrdinaryWork()
        log.debug(f"今日悬赏任务{work_list.total}个")
        for work in work_list.content:
            status = work_pb2.PlayStatus.Name(work.playStatus)
            if status == 'CAN_RECEIVE':
                # # 收取奖励
                # 获取任务详细信息
                work_info = client.GetOrdinaryWorkRecord(work.recordId)
                reward_info = client.ReceiveOrdinaryWorkReward(id=work.recordId)
                log.info("收取{}级任务{}，奖励:{}*{}".format(
                    work_info.level,
                    work_info.workName,
                    reward_info.rewards.scalarName,
                    reward_info.rewards.value)
                )
            elif status == 'NOT_STARTED':
                character_list = client.ListWorksCharacter()
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
                        client.PickOrdinaryWork(id=work.recordId, character_code=character.code)
                        # return
                        break
    else:
        log.info("公会悬赏暂时没有事情做")


def task_task(client):
    # 任务：助手每日任务
    log.info("「助手每日任务」执行中...")
    task_level = ["S", "A", "B", "C", "D"]
    for i in range(2):
        log.info("助手任务check...")
        task_list_character = client.ListTask(type="character")
        task_list_daily = client.ListTask(type="daily")
        task_list = [x for x in task_list_character.content] + [x for x in task_list_daily.content]
        for allow in task_level:
            for task in task_list:
                if task.level == allow:
                    status = param_pb2.PlayStatus.Name(task.status)
                    if status == 'CAN_RECEIVE':
                        # # 收取奖励
                        # 获取任务详细信息
                        task_info = client.GetTaskRecord(record_id=task.recordId)
                        reward_info = client.ReceiveTaskReward(id=task.recordId)
                        log.info("收取{}级任务{}，奖励:{}*{}".format(
                            task_info.level,
                            task_info.name,
                            reward_info.rewards.scalarName,
                            reward_info.rewards.value)
                        )
                    elif status == "NOT_STARTED":
                        # print(task.recordId)
                        task_info = client.GetTaskRecord(record_id=task.recordId)
                        character_list = client.ListTaskCharacter(id=task_info.id)
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
                                pick_info = client.PickTask(id=task_info.recordId, character_code=character.code)
                                log.info(f"参与成功,{pick_info.value}")
                                break
    else:
        log.info("助手任务暂时没有事情做")


def task_mail_receive(client):
    # 任务：邮件一键领取
    log.info("「邮件一键领取」任务执行中...")
    # # 获取邮件列表
    mail_list = client.ListMail()
    # print(mail_list)
    for mail in mail_list.content:
        if not mail.received:
            res = client.ReceiveAllMailAttachment()
            for reward in res.contents:
                log.info(f"邮件奖励获得：{reward.name}*{reward.num}")
            break
    else:
        log.info("邮件领取暂时没有事情做")


def task_coin_mall(client):
    # 任务：硬币商店
    log.info("「硬币商店」任务执行中...")
    # # 获取商店物品列表
    exchange_list = client.ListCoinExchangeRelation()
    for exchange in exchange_list.content:
        if exchange.target.materialCode in client.task.CoinMall['exchange_list']:
            times = exchange.maxTimes - exchange.userTimes
            log.debug(f"本周还可换取{times}次{exchange.target.materialName}")
            if exchange.maxTimes > exchange.userTimes:
                # # 兑换
                relation_code = exchange.relationCode
                relation_type = exchange.relationType
                log.info(f"硬币换取{times}次{exchange.target.materialName}")
                client.Exchange(
                    relation_code=relation_code,
                    relation_type=relation_type,
                    times=times
                )


def task_start(device_id, authorization):
    log.info("脚本执行中....")
    client = Client(device_id, authorization)
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
