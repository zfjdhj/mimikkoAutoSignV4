import os
import re
import sys
import time
import yaml
import grpc
import json
import hashlib
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED
from types import SimpleNamespace

from util.logger import Logger
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
import proto.scalar_pb2 as scalar_pb2
import proto.scalar_pb2_grpc as scalar_pb2_grpc
import proto.sign_pb2 as sign_pb2
import proto.sign_pb2_grpc as sign_pb2_grpc
import proto.signin_pb2 as signin_pb2
import proto.signin_pb2_grpc as signin_pb2_grpc
import proto.store_pb2 as store_pb2
import proto.store_pb2_grpc as store_pb2_grpc
import proto.task_pb2 as task_pb2
import proto.task_pb2_grpc as task_pb2_grpc
import proto.travelv2_pb2 as travelv2_pb2
import proto.travelv2_pb2_grpc as travelv2_pb2_grpc
import proto.work_pb2 as work_pb2
import proto.work_pb2_grpc as work_pb2_grpc

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
    def __init__(self, device_id='', authorization=''):
        self.cfg_file = 'config.yaml'
        self.host = 'api4.mimikko.cn'
        self.port = '443'
        self.agent = "okhttp/5.0.0-alpha.11"
        self.sdkversion = "4"
        self.is_login = True
        self.load_config(device_id, authorization)
        self.mimikko_version = self.basic.mimikko_version
        # 读取ssl证书
        with open('api4_mimikko_cn.cer', 'rb') as f:
            trusted_certs = f.read()
        credentials = grpc.ssl_channel_credentials(
            root_certificates=trusted_certs)
        # 设置最大消息接收长度8M
        MAX_MESSAGE_LENGTH = 8 * 1024 * 1024
        self.ssl_channel = grpc.secure_channel(
            target=self.host + ':' + self.port,
            credentials=credentials,
            options=(
                ('grpc.primary_user_agent', self.agent),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
            )
        )

    def load_config(self, device_id, authorization):
        with open(self.cfg_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.basic = SimpleNamespace(**config['Basic'])
        self.task = SimpleNamespace(**config['Task'])
        if self.basic.debug:
            log = Logger(
                base_path,
                base_path + f"/log/{date}.log",
                level="debug").logger
        else:
            log = Logger(
                base_path,
                base_path + f"/log/{date}.log",
                level="info").logger
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
                log.warning("更新config文件,原文件已备份config_old.yaml")
                with open(self.cfg_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    with open('config_old.yaml', 'w',
                              encoding='utf-8') as f_old:
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
        try:
            res = sub.__dict__[url_list[1]](
                pb2_.__dict__[request](**kw),
                compression=grpc.Compression.Gzip,
                metadata=self.metadata)
        except grpc.RpcError as e:
            log.error(f"call_api error: code={e.code()} message={e.details()}")
            login_text = ["阁下您已在别处登录啦>_<", "请勿重复点击登录按钮", "登录状态失效了( ͡• ͜ʖ ͡• )"]
            if e.details() in login_text:
                if self.login():
                    res = sub.__dict__[url_list[1]](
                        pb2_.__dict__[request](**kw),
                        compression=grpc.Compression.Gzip,
                        metadata=self.metadata)
                    return res
            elif e.details() == "Stream removed":
                log.debug("连接失败,重试中...")
                res = sub.__dict__[url_list[1]](
                    pb2_.__dict__[request](**kw),
                    compression=grpc.Compression.Gzip,
                    metadata=self.metadata)
                return res
        else:
            if not self.is_login:
                self.is_login = True
            # log.debug(grpc.StatusCode.OK)
            # sys.exit(0)
            return res


def task_sign(client):
    # 任务：每日签到
    if not client.is_login:
        return
    character_code = client.task.EnergyExchange["character_code"]
    res = ""
    log.info("「签到」任务执行中...")
    # 1.获取签到信息
    sign_info = client.call_api("Sign/GetUserSignStatus")
    res = "当前累计签到{}天, 今日{}签到".format(
        sign_info.continuousSign,
        '已' if sign_info.todaySign else '未'
    )
    log.info(res)
    if not sign_info.todaySign:
        # 2.签到
        log.info("今日还未签到，签到中...")
        client.call_api("Sign/Sign", **{"characterCode": character_code})
    return res


def task_energy_exchange(client):
    # 任务：成长值兑换
    if not client.is_login:
        return
    character_code = client.task.EnergyExchange["character_code"]
    log.info("「成长值兑换」任务执行中...")
    # # 获取能量值(用于兑换成长值)信息
    res = client.call_api("Scalar/GetUserAutoScalar",
                          **{"code": "user_energy"})
    if res.newValue > 0:
        character_code = client.task.EnergyExchange['character_code']
        res2 = client.call_api("Character/EnergyExchange",
                               characterCode=character_code)
        if res2.characterCode == character_code:
            log.info(f"{character_code}成长值兑换成功")
            # # 助手升级
            char_info = client.call_api(
                "Character/ListCharacter", page=1, pageSize=60)
            for char in char_info.content:
                if char.existNextLevel:
                    log.debug(f"存在后续等级{char.existNextLevel}")
                    for statistic in char.statistics:
                        if statistic.typeCode == 'character_favour':
                            if statistic.value > statistic.maxValue:
                                log.info(f"{char.name}满足升级条件，升级中....")
                                client.call_api(
                                    "Character/CharacterLevelManualUpgrade",
                                    code=char.code)
                # # 领取助手升级奖励
                if client.task.EnergyExchange["receive_level_reward"]:
                    sta = character_pb2.CharacterLevelRewardReplyStatus
                    reward_info = client.call_api(
                        "Character/ListCharacterLevelReward",
                        code=char.code, page=1, pageSize=60)
                    for reward in reward_info.content:
                        status = sta.Name(reward.status)
                        if status == "AVAILABLE":
                            reward_detail = ""
                            for r in reward.rewards:
                                reward_detail += f"{r.name}*{r.num} "
                            log.info("{}领取{}奖励：{}".format(
                                char.name,
                                reward.level,
                                reward_detail
                            ))
                            client.call_api(
                                "Character/ReceiveCharacterLevelReward",
                                levelId=reward.levelId,
                                rewardCollectionId=reward.rewardCollectionId)

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
        res = client.call_api(
            "Energy/ListEnergySourceRecord", page=1, pageSize=60)
        for i in res.content:
            status = energy_pb2.Status.Name(i.status)
            if status == 'FINISHED':
                # # # 领取
                client.call_api(
                    "Energy/ReceiveEnergySourceReward", id=i.id)
                log.info(f'能源中心领取{i.position+1}号位')
                continue
            elif status == 'UNLOCKED':
                # # # 创建
                res3 = client.call_api(
                    "Energy/ListEnergySourceModel", page=1, pageSize=60)
                if client.task.EnergyCenter['auto_use_energy_speedup_ticket']:
                    # 判断 电力充能券数量
                    res = client.call_api(
                        "Scalar/GetUserMaterialScalar",
                        scalarCode="_scalar_material_amount",
                        materialCode="energy_speedup_ticket")
                    source_mode = '超级芯片' if res.integerValue > 0 else "普通芯片"
                    log.debug(f"电力充能券：{res.integerValue}")
                else:
                    source_mode = '普通芯片'
                for item in res3.content:
                    if item.name == source_mode:
                        # ## 创建充能
                        client.call_api(
                            "Energy/CreateEnergySourceRecord",
                            modelId=item.modelId, position=i.position)
                        log.info(f'能源中心创建充能{i.position+1}号位({source_mode})')
                continue
    else:
        log.info("能源中心暂时没有事情做")


def task_ordinary_work(client):
    # 任务：公会悬赏任务
    if not client.is_login:
        return
    log.info("「公会悬赏」任务执行中...")
    log.info("公会悬赏任务check...")
    work_list = client.call_api(
        "Work/ListOrdinaryWork", page=1, pageSize=60)
    log.debug(f"今日悬赏任务{work_list.total}个")
    # 收取已完成任务奖励
    for work in work_list.content:
        status = work_pb2.PlayStatus.Name(work.playStatus)
        if status == 'CAN_RECEIVE':
            # # 收取奖励
            # 获取任务详细信息
            work_info = client.call_api(
                "Work/GetOrdinaryWorkRecord", id=work.recordId)
            reward_info = client.call_api(
                "Work/ReceiveOrdinaryWorkReward", id=work.recordId)
            log.info("收取{}级任务{}，奖励:{}*{}".format(
                work_info.level,
                work_info.workName,
                reward_info.rewards.scalarName,
                reward_info.rewards.value)
            )
    # 领取任务
    for work in work_list.content:
        status = work_pb2.PlayStatus.Name(work.playStatus)
        if status == 'NOT_STARTED':
            character_list = client.call_api(
                "Work/ListWorksCharacter", page=1, pageSize=60)
            log.debug(f"当前空闲助手{character_list.total}个")
            work_characters = client.task.OrdinaryWork["work_characters"]
            for character in character_list.content:
                if character.code in work_characters:
                    # 判断是否能源值充足24h*20=480
                    if client.task.OrdinaryWork[
                            "auto_use_energy_pack"]["enable"]:
                        energy_now = client.call_api(
                            "Scalar/GetUserScalar",
                            code="user_enegry_source").integerValue
                        if int(energy_now) > client.task.OrdinaryWork[
                                "auto_use_energy_pack"]["energy_min"]:
                            log.debug(f"当前电力充足{energy_now}")
                        else:
                            log.info(f"当前电力不足{energy_now}")
                            energy_pack_list = {
                                "energy_pack_s": {
                                    "relationCode": "energy_s",
                                    "value": 50
                                },
                                "energy_pack_m_2": {
                                    "relationCode": "energy_m_2",
                                    "value": 300
                                },
                                "energy_pack_m_1": {
                                    "relationCode": "energy_m_1",
                                    "value": 500,
                                },
                                "energy_pack_l": {
                                    "relationCode": "energy_l",
                                    "value": 1000
                                },
                            }
                            itemlist = client.call_api(
                                "Material/ListMaterial",
                                materialTypeCode="consumable",
                                isOwn=1,
                                page=1,
                                pageSize=60
                            )
                            for item in itemlist.content[::-1]:
                                if item.code in energy_pack_list:
                                    energy_max = client.task.OrdinaryWork[
                                        "auto_use_energy_pack"
                                    ]["energy_max"]
                                    use = (
                                        energy_max - energy_now) // (
                                            energy_pack_list[
                                                item.code]["value"])
                                    times = min(use, item.statistics.value)
                                    log.info(f"补充电力:{item.name}*{times}")
                                    client.call_api(
                                        "Scalar/Exchange",
                                        relationCode=energy_pack_list[
                                            item.code]["relationCode"],
                                        relationType="common",
                                        times=times
                                    )
                                    break
                    log.info("{}将被派往执行{}级任务{}，奖励:{}*{}".format(
                        character.name,
                        work.level,
                        work.name,
                        work.rewards.scalarName,
                        work.rewards.value
                    ))
                    client.call_api(
                        "Work/PickOrdinaryWork",
                        body={"characterCode": character.code},
                        id=work.recordId)
                    break
    else:
        log.info("公会悬赏暂时没有事情做")


def task_task(client):
    # 任务：助手每日任务
    if not client.is_login:
        return
    log.info("「助手每日任务」执行中...")
    log.info("助手任务check...")
    task_list_character = client.call_api(
        "Task/ListTask", type="character", page=1, pageSize=60)
    task_list_daily = client.call_api(
        "Task/ListTask", type="daily", page=1, pageSize=60)
    task_list = [x for x in task_list_character.content] + \
        [x for x in task_list_daily.content]
    # 收取已完成任务奖励
    for task in task_list:
        status = param_pb2.PlayStatus.Name(task.status)
        if status == 'CAN_RECEIVE':
            # 收取奖励
            # 获取任务详细信息
            task_info = client.call_api(
                "Task/GetTaskRecord", id=task.recordId)
            reward_info = client.call_api(
                "Task/ReceiveTaskReward", id=task.recordId)
            log.info("收取{}级任务{}，奖励:{}*{}".format(
                task_info.level,
                task_info.name,
                reward_info.rewards.scalarName,
                reward_info.rewards.value)
            )
    # 领取任务
    task_level = ["S", "A", "B", "C", "D"]
    for level in task_level:
        for task in task_list:
            if task.level != level:
                continue
            status = param_pb2.PlayStatus.Name(task.status)
            if status == "NOT_STARTED":
                task_info = client.call_api(
                    "Task/GetTaskRecord", id=task.recordId)
                character_list = client.call_api(
                    "Task/ListTaskCharacter",
                    id=task_info.id, page=1, pageSize=60)
                log.debug(
                    f"{task.level}级任务，可参与助手{character_list.total}个")
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
                            "Task/PickTask", id=task_info.recordId,
                            body={"characterCode": character.code})
                        log.info(f"参与成功,{pick_info.value}")
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
    exchange_list = client.call_api(
        "Scalar/ListCoinExchangeRelation", page=1, pageSize=60)
    for exchange in exchange_list.content:
        if exchange.target.materialCode in client.task.CoinMall[
                'exchange_list']:
            times = exchange.maxTimes - exchange.userTimes
            log.debug(f"本周还可换取{times}次{exchange.target.materialName}")
            if exchange.maxTimes > exchange.userTimes:
                # # 兑换
                buy_item(client, exchange.target.materialCode, times)
                log.info(f"硬币换取{times}次{exchange.target.materialName}")


def task_activity_sign(client):
    # 任务：活动签到
    if not client.is_login:
        return
    log.info("「活动签到」任务执行中...")
    # 获取活动 i1 id
    acts = client.call_api(
        api_url='ActivityNew/ListActivityNew',
        content_type='application/grpc-web-text',
        **{
            'typeCode': 'signin_activity',
            'page': 1,
            'pageSize': 20
        })
    # 今日是否签到
    sign_info = client.call_api(
        api_url='ActivityNew/GetTodayAvailableSign')
    for act in acts.content:
        if act.id in sign_info.ids:
            sign = client.call_api(
                api_url='SignIn/SignIn',
                content_type='application/grpc-web-text',
                **{'activityId': act.id}
            )
            log.info(f'「{act.name}」活动签到中...')
            if sign.success:
                log.info('活动签到成功')
            else:
                log.error('活动签到失败')
        else:
            log.info(f'「{act.name}」今日已签到')


def get_character_json(path):
    res = {}
    try:
        with open(path, encoding='utf-8') as f:
            res = json.loads(f.read())
    except Exception as e:
        log.warning(e)
    return res


def get_cname_en(client, name_zh):
    resp = client.call_api(
        api_url='Material/ListHandbookCharacter',
        **{
            'materialTypeCode': 'clothes',
            'page': 1,
            'pageSize': 60
        }
    )
    for c in resp.content:
        if c.material.name == name_zh:
            if c.material.code:
                return c.material.code


def get_new_character(client, data, path):
    res = []
    tmpd = {}
    for type, c in data.items():
        tmpd.update(c)
    resp = client.call_api(
        api_url='Store/ListTagSift',
        content_type='application/grpc-web-text'
    )
    for e in resp.tagCategories:
        if e.categoriesId in [2153, 2156]:
            for tag in e.tags:
                if tag.value not in tmpd.keys():
                    cname_en = get_cname_en(client, tag.value)
                    if get_cname_en:
                        res.append({e.categoriesName: {tag.value: cname_en}})
                    else:
                        log.warning(f'更新{tag.value}失败')
    return res


def write_character_json(old_data, new_character_data, path):
    for new_c in new_character_data:
        for k, v in new_c.items():
            if old_data.get(k):
                old_data[k].update(v)
            else:
                old_data.update({k: v})
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(old_data, ensure_ascii=False, indent=4))


def task_update_character_json(client):
    # 任务：更新助手列表
    if not client.is_login:
        return
    log.info("「助手列表」更新中...")
    path = './助手列表.json'
    old_data = get_character_json(path)
    new_character_data = get_new_character(client, old_data, path)
    if new_character_data:
        log.info(f'新助手：{new_character_data}')
        write_character_json(old_data, new_character_data, path)
    else:
        log.info("暂时没有更新新的助手")


def list_travel_record(client):
    resp = client.call_api(
        api_url='TravelV2/ListTravelRecord',
        **{'page': 1,
            'pageSize': 60
           }
    )
    for t in resp.content:
        remain_time_s = t.travelGroup.totalTime - t.travelGroup.upTime
        if remain_time_s > 86400:
            remain_time = str(remain_time_s // 86400) + 'day'
        else:
            remain_time = ''
        remain_time += time.strftime("%H:%M:%S", time.gmtime(remain_time_s))
        total_time_s = t.travelGroup.totalTime
        if total_time_s > 86400:
            total_time = str(total_time_s // 86400) + 'day'
        else:
            total_time = ''
        total_time += time.strftime("%H:%M:%S", time.gmtime(total_time_s))
        date = time.strftime(
            "%Y-%m-%d-[%H:%M:%S]",
            time.localtime(t.travelGroup.endTime.seconds))
        status = param_pb2.PlayStatus.Name(
            t.travelGroup.status)
        characters = [x.name for x in t.travelGroup.travelingCharacters]
        log.info(
            "{}{}[{}]:{},剩余时间:{}/{},结束时间:{}".format(
                t.travelArea.areaName,
                t.travelGroup.name,
                status,
                characters,
                remain_time,
                total_time,
                date))
    return resp


def list_travel_area(client):
    resp = client.call_api(
        api_url='TravelV2/ListTravelArea',
        **{'page': 1,
            'pageSize': 60
           }
    )
    return resp


def get_areaid_groupid(client, area_name, group_name):
    areas = list_travel_area(client).content
    area_id = 0
    group_id = 0
    for area in areas:
        if area.areaName == area_name:
            area_id = area.areaId
            resp = client.call_api(
                api_url='TravelV2/ListTravelGroup',
                **{'areaId': area.areaId,
                    'page': 1,
                   'pageSize': 60
                   }
            )
            for group in resp.content:
                if group.name == group_name:
                    group_id = group.id
                    break
            break
    return area_id, group_id


def calculate_travel_consume(client, area_id, group_id, character_codes):
    if not character_codes:
        log.error('task_tavel:character_codes为空')
    resp = client.call_api(
        api_url='TravelV2/CalculateTravelConsume',
        **{'areaId': area_id,
            'groupId': group_id,
            'characterCodes': character_codes
           }
    )
    return resp


def list_travels_character(client, group_id):
    resp = client.call_api(
        api_url='TravelV2/ListTravelsCharacter',
        **{
            'groupId': group_id,
            'page': 1,
            'pageSize': 60
        }
    )
    return resp


def buy_item(client, materialCode, num):
    exchange_list = client.call_api(
        "Scalar/ListCoinExchangeRelation", page=1, pageSize=60)
    for exchange in exchange_list.content:
        if exchange.target.materialCode == materialCode:
            # 购买物品
            client.call_api("Scalar/Exchange",
                            relationCode=exchange.relationCode,
                            relationType=exchange.relationType,
                            times=num)
            return True
    else:
        log.error(f'购买{materialCode}失败')
        return False


def get_item(client, materialCode, materialTypeCode='consumable', num=0):
    itemlist = client.call_api("Material/ListMaterial",
                               materialTypeCode=materialTypeCode,
                               isOwn=1,
                               page=1,
                               pageSize=60
                               )
    for item in itemlist.content[::-1]:
        if item.code == materialCode:
            if item.statistics.value >= num:
                log.info(f'背包中{item.name}*{item.statistics.value},物品充足。')
                return True
            else:
                if num:
                    log.info(f'背包中{item.name}不足，商店购买中...')
                    return buy_item(client, materialCode, num)
            break
    else:
        if num:
            log.info(f'背包中{materialCode}不足，商店购买中...')
            return buy_item(client, materialCode, num)


def cal_travel_gift(client, area_name, group_name, aid, gid):
    # 获取背包纪念品列表
    own_gift_list = []
    res = client.call_api('Material/ListMaterial', **{
        'materialTypeCode': 'gift',
        'isOwn': 1, 'page': 1,
        'pageSize': 60})
    for item in res.content:
        own_gift_list.append(item.name)
    # 获取当前选择区域纪念品列表
    possible_rewards = []
    group_info = client.call_api(
        "TravelV2/GetTravelGroup", ** {'areaId': aid, 'groupId': gid})
    for item in group_info.travelGroup.possibleRewards:
        possible_rewards.append(item.materialName)
    # 尚未获得
    do_not_have = set(possible_rewards)-set(own_gift_list)
    log.info('{}{}纪念品收集进度({}/{}),未收集列表{}'.format(
        area_name, group_name,
        len(possible_rewards)-len(do_not_have),
        len(possible_rewards),
        do_not_have
    ))


def cal_travel_postcard(client, area_name, group_name, aid, gid, characters):
    # 获取背包明信片列表
    own_postcard_list = []
    for c in characters:
        res = client.call_api('Material/ListHandbookMaterialByCharacterCode',
                              **{'code': c,
                                 "typeCode": "postcard",
                                 "page": 1,
                                 "pageSize": 60})
        for postcard in res.content:
            if postcard.statistics.value:
                own_postcard_list.append(postcard.statistics.typeName)
    # 获取当前选择区域明信片列表
    possible_rewards = []
    reward_info = client.call_api(
        "TravelV2/ListTravelGroupReward", ** {'groupId': gid})
    for postcard in reward_info.postCards:
        for c in characters:
            if c in postcard.materialCode:
                possible_rewards.append(postcard.materialName)
    # print(possible_rewards)
    # 尚未获得
    do_not_have = set(possible_rewards)-set(own_postcard_list)
    log.info('{}{}选定助手明信片收集进度({}/{}),未收集列表{}'.format(
        area_name, group_name,
        len(possible_rewards)-len(do_not_have),
        len(possible_rewards),
        do_not_have
    ))


def task_travel(client):
    # 任务：助手出游
    if not client.is_login:
        return
    log.info("「助手出游」任务执行中...")
    character_codes = client.task.Travel['travel_characters']
    area_name = client.task.Travel['travel_area']
    group_name = client.task.Travel['travel_group']
    # 获取当前出游列表
    travel_list = list_travel_record(client)
    for travel in travel_list.content:
        if travel.travelGroup.status == 2:
            # 收取奖励
            resp = client.call_api('TravelV2/ReceiveTravelReward',
                                   **{"id": travel.recordId})
            res = "获得:"
            reward_l = []
            for reward in resp.rewards:
                if reward.scalarName:
                    reward_l.append(reward.materialName +
                                    reward.scalarName +
                                    "*" + str(reward.value))
                else:
                    reward_l.append(reward.materialName +
                                    "*" + str(reward.value))
            res += ",".join(reward_l)
            log.info(res)
            pass
    # 获取剩余可出游次数
    for area in list_travel_area(client).content:
        if area.areaName == area_name:
            if not area.characterIdleAmount:
                log.info('暂时没有出游次数')
                return
            else:
                log.debug(f'出游次数:{area.characterIdleAmount}')
    # 尝试开始新的出游
    aid, gid = get_areaid_groupid(client,
                                  area_name, group_name)
    for i in range(3):
        # 空闲助手[默认同时每次一个角色][vip每次两个角色]
        travel_characters = []
        cl = list_travels_character(client, gid).content
        for c in cl:
            if c.code in character_codes:
                travel_characters.append(c.code)
        if not travel_characters:
            log.info('当前没有空闲助手')
            return
        # 计算消耗
        if client.task.Travel["character_upper_limit"]:
            character_num = client.task.Travel["character_upper_limit"]
            log.debug(f"config指定出发人数{character_num}")
        else:
            group_info = client.call_api(
                "TravelV2/GetTravelGroup", ** {'areaId': aid, 'groupId': gid})
            character_num = group_info.characterUpperLimit
        if len(travel_characters) < character_num:
            log.error("当前空闲助手数量不足({}/{})，会造成消耗浪费！".format(
                len(travel_characters),
                character_num
            ))
            return
        consume = calculate_travel_consume(
            client, aid, gid, travel_characters[:character_num]
        ).travelConsumes[0]
        log.info('{}{}{}消耗{}*{}'.format(
            area_name, group_name,
            travel_characters[:character_num],
            consume.materialName,
            consume.attributes['number']
        ))
        # 判断背包物品是否充足
        if not get_item(client,
                        consume.materialCode,
                        materialTypeCode='consumable',
                        num=character_num):
            log.error('判断物品充足失败')
            return
        # 开始出游
        log.info(f'{travel_characters[:character_num]}开始出游')
        client.call_api('TravelV2/Travel', **{
            'areaId': aid,
            'travelGroupId': gid,
            'characterCode': travel_characters[:character_num]
        })
        # 输出显示纪念品/明信片收集列表
        if group_name != '时光之旅':
            cal_travel_gift(client, area_name, group_name, aid, gid)
            cal_travel_postcard(client, area_name, group_name,
                                aid, gid, travel_characters[:character_num])
        else:
            cal_travel_postcard(client, area_name, group_name,
                                aid, gid, travel_characters[:character_num])
        # 获取当前出游列表
        list_travel_record(client)


def camel_to_snake(camel):
    underscore = re.sub('([A-Z])', r'_\1', camel).lower()
    return underscore[1:] if underscore.startswith("_") else underscore


def task_start(device_id, authorization):
    client = Client(device_id, authorization)
    log.info("脚本执行中....")
    if client.is_login:
        for task_name in client.task.__dict__:
            if client.task.__dict__[task_name]['enable']:
                task = globals()['task_' + camel_to_snake(task_name)]
                task(client)
        log.info("脚本执行结束....")
        return client
    else:
        log.info("登录中....")
        client.login()
        if client.is_login:
            return task_start(client)


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
        scheduler.add_job(
            task_start, 'interval',
            hours=interval_hours,
            args=[device_id, authorization])
        scheduler.add_listener(job_execute, EVENT_JOB_EXECUTED)
        scheduler.start()


if __name__ == '__main__':
    main(device_id, authorization)
