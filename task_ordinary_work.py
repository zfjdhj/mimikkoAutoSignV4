import time
import datetime

import proto.work_pb2 as work_pb2


def task_ordinary_work(client, log):
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
        # 等待6分钟接近完成任务
        if work.endAt.seconds:
            wait_s = int(work.endAt.seconds - time.time())
            if 0 < wait_s < 0.1 * client.basic.scheduler_interval * 3600:
                log.info(f'[{work.name}]即将完成，等待{wait_s}s')
                time.sleep(wait_s)
                task_ordinary_work(client, log)
                return
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
    # 刷新列表
    content = use_work_refresh_ticket(client, log, work_list.content)
    # 领取任务
    for work in content:
        status = work_pb2.PlayStatus.Name(work.playStatus)
        if status == 'NOT_STARTED':
            character_list = client.call_api(
                "Work/ListWorksCharacter", page=1, pageSize=60)
            log.debug(f"[{work.name}]当前空闲助手{character_list.total}个")
            if not character_list.total:
                break
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
    log.info("公会悬赏暂时没有事情做")


def use_work_refresh_ticket(client, log, content):
    if not client.task.OrdinaryWork['auto_use_work_refresh_ticket'] or len(client.task.OrdinaryWork['work_characters']) < 2:
        return content
    else:
        content = list(reversed(content))
        now = datetime.datetime.now()
        remain_time_18 = (18 - now.hour) * 3600 - now.minute * 60 - now.second
        if remain_time_18 < 0:
            log.debug('下午18点后不适合使用工作刷新券')
            return content
        remain_time = 0
        on_going_work = []
        for work in content:
            if work.playStatus == 1:
                remain_time += int(work.endAt.seconds - time.time())
                on_going_work.append(work)
            elif work.playStatus == 0:
                log.debug('尚有工作未完成，不适合刷新')
                return content
        log.debug(
            f'remain_time:{remain_time},on_going_work:{len(on_going_work)},remain_time_18:{remain_time_18}')
        if remain_time - len(on_going_work) * remain_time_18 > 0:
            log.debug('18点前工作未全部完成，不适合使用工作刷新券')
        else:
            log.info('可以使用工作刷新券')
            # 判断工作刷新券数量
            res = client.call_api(
                "Scalar/GetUserMaterialScalar",
                scalarCode="_scalar_material_amount",
                materialCode="_work_refresh_ticket")
            if res.integerValue:
                log.info(f"工作刷新券：{res.integerValue}，使用中...")
                # 使用工作刷新券
                client.call_api(
                    "Work/Refresh")
                # 刷新列表
                work_list = client.call_api(
                    "Work/ListOrdinaryWork", page=1, pageSize=60)
                res = list(reversed(work_list.content))
                return res
            else:
                log.info('工作刷新券数量不足')
                return content
        return content


if __name__ == '__main__':
    import os
    from main import Client
    from util.logger import Logger

    # log信息配置

    base_path = os.path.dirname(os.path.abspath(__file__))

    if base_path == "":
        base_path = "/home/runner/work/mimikkoAutoSignIn/mimikkoAutoSignIn"
        os.system(f"chmod 777 {base_path}")
    if not os.path.exists(base_path + "/log"):
        os.makedirs(f"{base_path}/log", mode=777)
        os.system(f"chmod 777 {base_path}/log")
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    log = Logger(base_path,
                 base_path + f"/log/{date}.log",
                 level="debug").logger

    client = Client()
    task_ordinary_work(client, log)
