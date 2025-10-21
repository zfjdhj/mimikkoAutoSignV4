import os
import time

import proto.param_pb2 as param_pb2
from task.task_update_character_json import get_cname_json
from util.logger import Logger

def safe_hms(seconds) -> str:
    try:
        sec = int(seconds)
    except Exception:
        sec = 0
    if sec < 0:
        sec = 0
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

base_path = os.path.dirname(os.path.abspath(__file__))
travel_log = Logger(
    base_path,
    os.path.abspath("./log/travel.log"),
    level="debug",
    screen=False,
    when='').logger


def task_travel(client):
    # 任务：助手出游
    if not client.is_login:
        return
    log = client.log
    log.info("「助手出游」任务执行中...")
    character_cfg = client.task.Travel['travel_characters']
    all_character_codes = character_cfg.keys()
    areas_name = client.task.Travel['travel_areas']
    # 获取当前出游列表
    travel_list = list_travel_record(client)
    for travel in travel_list.content:
        # 等待300秒即将完成的任务
        if travel.travelGroup.endTime:
            wait_s = int(travel.travelGroup.endTime.seconds - time.time())
            if 0 < wait_s < client.task.Travel['wait_for_finish']:
                log.info(
                    f'{[x.name for x in travel.travelGroup.travelingCharacters]}[{travel.travelGroup.name}]即将完成，等待{wait_s}s')
                time.sleep(wait_s)
                return client.task.Travel['then_do_task']
        if travel.travelGroup.status == 2:
            # 收取奖励
            resp = client.call_api('TravelV2/ReceiveTravelReward',
                                   **{"id": travel.recordId})
            res = "获得:"
            reward_l = []
            for reward in resp.rewards:
                if reward.scalarName:
                    reward_l.append(
                        reward.materialName + reward.scalarName + "*" + str(reward.value))
                else:
                    reward_l.append(
                        reward.materialName + "*" + str(reward.value))
            for reward in resp.postCards:
                if reward.scalarName:
                    if reward.materialName + reward.scalarName + "*" + str(reward.value) not in reward_l:
                        reward_l.append(
                            reward.materialName + reward.scalarName + "*" + str(reward.value))
                elif reward.materialName + "*" + str(reward.value) not in reward_l:
                    reward_l.append(
                        reward.materialName + "*" + str(reward.value))
            res += ",".join(reward_l)
            log.info(res)
            # travel_log.info(str(resp))
            travel_log.info(res)
            if client.task.Travel["exchange_postcard"]:
                exchange_postcard(client)
    # 整理出游列表
    travel_list = {}
    for c in character_cfg:
        area_tmp = character_cfg[c]["travel_area"]
        group_tmp = character_cfg[c]["travel_group"]
        if not travel_list.get(area_tmp):
            travel_list[area_tmp] = {}
        if not travel_list[area_tmp].get(group_tmp):
            travel_list[area_tmp][group_tmp] = []
        travel_list[area_tmp][group_tmp].append(c)
    # 获取剩余可出游次数
    travel_area_info = list_travel_area(client).content
    log.info(f'阁下还可以指定[{travel_area_info[0].characterIdleAmount}]个助手出游~')
    if not travel_area_info[0].characterIdleAmount:
        return
    for i in range(travel_area_info[0].characterIdleAmount):
        for area_name in [x for x in travel_list.keys()]:
            travel_area_info = list_travel_area(client).content
            for area in travel_area_info:
                if area.areaName == area_name:
                    if not travel_list[area_name]:
                        break
                    if not area.areaTravelRemainAmount:
                        log.info(f'{area.areaName}暂时没有出游次数')
                        if not client.task.Travel['auto_next_area']:
                            break
                        next_area = areas_name[(areas_name.index(
                            area_name) + 1) % len(areas_name)]
                        log.info(f'{travel_list[area_name]}移动至下一区域{next_area}')
                        if not travel_list.get(next_area):
                            travel_list[next_area] = travel_list[area_name]
                            travel_list[area_name] = {}
                        else:
                            for group in travel_list[area_name]:
                                if not travel_list[next_area].get(group):
                                    travel_list[
                                        next_area][group] = travel_list[
                                            area_name][group]
                                else:
                                    for c in travel_list[area_name][group]:
                                        travel_list[next_area][group].append(c)
                        break
                    else:
                        log.debug('{}剩余出游次数{}'.format(
                            area.areaName,
                            area.areaTravelRemainAmount
                        ))
            else:
                if not travel_list.get(area_name):
                    continue
                for group_name in travel_list[area_name]:
                    # 尝试开始新的出游
                    aid, gid = get_areaid_groupid(client,
                                                  area_name, group_name)
                    character_codes = travel_list[area_name][group_name]
                    # 空闲助手[默认同时每次一个角色][vip每次两个角色]
                    travel_characters = []
                    cl = list_travels_character(client, gid).content
                    break_circle = True
                    for c in cl:
                        if c.code in character_codes:
                            travel_characters.append(c.code)
                        if c.code in all_character_codes:
                            break_circle = False
                    if not cl or break_circle:
                        log.info('当前没有空闲助手')
                        return
                    if not travel_characters:
                        log.info('当前区域旅行模式没有适合助手')
                        break
                    # 计算消耗
                    if client.task.Travel["character_upper_limit"]:
                        character_num = client.task.Travel[
                            "character_upper_limit"]
                        log.debug(f"config指定出发人数{character_num}")
                    else:
                        group_info = client.call_api(
                            "TravelV2/GetTravelGroup",
                            ** {'areaId': aid, 'groupId': gid})
                        character_num = group_info.characterUpperLimit
                    if len(travel_characters) < character_num:
                        log.error("当前空闲助手数量不足({}/{})，可能造成出游次数浪费".format(
                            len(travel_characters),
                            character_num
                        ))
                        log.info("config:character_upper_limit:1设置项取消此提示")
                        return
                    name = get_cname_json(
                        log, travel_characters[:character_num], [])
                    consume = calculate_travel_consume(
                        client, aid, gid, travel_characters[:character_num]
                    ).travelConsumes[0]
                    log.info('{}{}{}消耗{}*{}'.format(
                        area_name, group_name,
                        name,
                        consume.materialName,
                        consume.attributes['number']
                    ))
                    # 判断背包物品是否充足
                    if not get_item(client,
                                    consume.materialCode,
                                    consume.materialName,
                                    materialTypeCode='consumable',
                                    num=character_num):
                        log.error('判断物品充足失败')
                        return
                    # 开始出游
                    log.info(f'{name}开始出游')
                    client.call_api('TravelV2/Travel', **{
                        'areaId': aid,
                        'travelGroupId': gid,
                        'characterCode': travel_characters[:character_num]
                    })
                    # 输出显示纪念品/明信片收集列表
                    if group_name != '时光之旅':
                        cal_travel_gift(client, area_name,
                                        group_name, aid, gid)
                        cal_travel_postcard(client, area_name, group_name,
                                            aid, gid,
                                            travel_characters[:character_num])
                    else:
                        cal_travel_postcard(client, area_name, group_name,
                                            aid, gid,
                                            travel_characters[:character_num])
                    # 获取当前出游列表
                    list_travel_record(client)


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
        remain_time += safe_hms(remain_time_s)
        total_time_s = t.travelGroup.totalTime
        if total_time_s > 86400:
            total_time = str(total_time_s // 86400) + 'day'
        else:
            total_time = ''
        total_time += safe_hms(total_time_s))
        date = time.strftime(
            "%Y-%m-%d-[%H:%M:%S]",
            time.localtime(t.travelGroup.endTime.seconds))
        status = param_pb2.PlayStatus.Name(
            t.travelGroup.status)
        characters = [x.name for x in t.travelGroup.travelingCharacters]
        client.log.info(
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
        client.log.error('task_tavel:character_codes为空')
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


def buy_item(client, materialCode, materialName, num, relation_code=""):
    exchange_list = client.call_api(
        "Scalar/ListCoinExchangeRelation", page=1, pageSize=60)
    for exchange in exchange_list.content:
        if relation_code:
            if exchange.relationCode == relation_code:
                # 购买物品
                client.call_api("Scalar/Exchange",
                                relationCode=exchange.relationCode,
                                relationType=exchange.relationType,
                                times=num)
                return True
        elif exchange.target.materialCode == materialCode:
            # 购买物品
            client.call_api("Scalar/Exchange",
                            relationCode=exchange.relationCode,
                            relationType=exchange.relationType,
                            times=num)
            return True
    else:
        client.log.error(f'购买{materialName}失败')
        return False


def get_item(client, materialCode, materialName, materialTypeCode='consumable', num=0):
    itemlist = client.call_api("Material/ListMaterial",
                               materialTypeCode=materialTypeCode,
                               isOwn=1,
                               page=1,
                               pageSize=60
                               )
    for item in itemlist.content[::-1]:
        if item.code == materialCode:
            if item.statistics.value >= num:
                client.log.info(
                    f'背包中{item.name}*{item.statistics.value},物品充足。')
                return True
            else:
                if num:
                    client.log.info(f'背包中{item.name}不足，商店购买中...')
                    return buy_item(client, materialCode, materialName, num)
            break
    else:
        if num:
            client.log.info(f'背包中{materialName}不足，商店购买中...')
            return buy_item(client, materialCode, materialName, num)


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
    do_not_have = set(possible_rewards) - set(own_gift_list)
    client.log.info('{}{}纪念品收集进度({}/{}),未收集列表{}'.format(
        area_name, group_name,
        len(possible_rewards) - len(do_not_have),
        len(possible_rewards),
        do_not_have
    ))
    travel_log.info('{}{}纪念品收集进度({}/{}),未收集列表{}'.format(
        area_name, group_name,
        len(possible_rewards) - len(do_not_have),
        len(possible_rewards),
        do_not_have
    ))


def cal_travel_postcard(client, area_name, group_name, aid, gid, characters):
    # 获取背包明信片列表
    own_postcard_list = []
    characters_name = []
    for c in characters:
        res = client.call_api('Material/ListHandbookMaterialByCharacterCode',
                              **{'code': c,
                                 "typeCode": "postcard",
                                 "page": 1,
                                 "pageSize": 60})
        for postcard in res.content:
            if postcard.statistics.value:
                own_postcard_list.append(postcard.statistics.typeName)
            if postcard.attributes.get('characterName'):
                if postcard.attributes['characterName'] not in characters_name:
                    characters_name.append(
                        postcard.attributes['characterName'])
    if not characters_name:
        characters_name = get_cname_json(client.log, characters)
    # 获取当前选择区域明信片列表
    possible_rewards = []
    reward_info = client.call_api(
        "TravelV2/ListTravelGroupReward", ** {'groupId': gid})
    for postcard in reward_info.postCards:
        for c in characters:
            if c in postcard.materialCode:
                possible_rewards.append(postcard.materialName)
    # 尚未获得
    do_not_have = set(possible_rewards) - set(own_postcard_list)
    client.log.info('{}{}{}明信片收集进度({}/{}),未收集列表{}'.format(
        area_name, group_name,
        characters_name,
        len(possible_rewards) - len(do_not_have),
        len(possible_rewards),
        do_not_have
    ))
    travel_log.info('{}{}{}明信片收集进度({}/{}),未收集列表{}'.format(
        area_name, group_name,
        characters_name,
        len(possible_rewards) - len(do_not_have),
        len(possible_rewards),
        do_not_have
    ))


def exchange_postcard(client):
    # 获得背包时光碎片数量
    res = client.call_api(
        "Scalar/GetUserMaterialScalar",
        scalarCode="_scalar_material_amount",
        materialCode="time_ticket")
    if res.integerValue < 5:
        client.log.info(f"当前时光碎片数量：{res.integerValue}")
    else:
        # 兑换
        res = client.call_api(
            "TravelV2/ExchangePostcard")
        travel_log.debug(str(res))
        if res.name:
            client.log.info(f"时光碎片兑换成功，恭喜获得：{res.name}")

