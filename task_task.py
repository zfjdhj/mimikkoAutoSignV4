import time

import proto.param_pb2 as param_pb2


def task_task(client, log):
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
        # 等待6分钟接近完成任务
        if task.remainingTime:
            wait_s = int(task.remainingTime - time.time())
            if 0 < wait_s < 0.1 * client.basic.scheduler_interval * 3600:
                log.info(f'{task.name}即将完成，等待{wait_s}s')
                time.sleep(wait_s)
                task_task(client, log)
                return
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
                if not task.characterLimit and not character_list.total:
                    log.debug('暂时没有空闲助手')
                    break
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
            continue
        break
    log.info("助手任务暂时没有事情做")


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
    task_task(client, log)
