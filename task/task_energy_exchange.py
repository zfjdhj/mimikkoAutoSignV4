import proto.character_pb2 as character_pb2

from task.task_update_character_json import get_cname_json


def task_energy_exchange(client):
    # 任务：成长值兑换
    if not client.is_login:
        return
    log = client.log
    character_code = client.task.EnergyExchange["character_code"]
    log.info("「成长值兑换」任务执行中...")
    # # 获取能量值(用于兑换成长值)信息
    res = client.call_api("Scalar/GetUserAutoScalar",
                          **{"code": "user_energy"})
    if res.newValue > 0:
        character_code = client.task.EnergyExchange['character_code']
        res2 = client.call_api("Character/EnergyExchange",
                               characterCode=character_code)
        name = get_cname_json(log, character_code)
        if res2.characterCode == character_code:
            log.info(f"「{name}」成长值兑换成功")
            # # 助手升级
            char_info = client.call_api(
                "Character/ListCharacter", page=1, pageSize=60)
            for char in char_info.content:
                if char.existNextLevel:
                    log.debug("存在后续等级")
                    for statistic in char.statistics:
                        if statistic.typeCode == 'character_favour':
                            if statistic.value > statistic.maxValue:
                                log.info(f"「{char.name}」满足升级条件，升级中....")
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
                            log.info("「{}」领取{}奖励：{}".format(
                                char.name,
                                reward.level,
                                reward_detail
                            ))
                            client.call_api(
                                "Character/ReceiveCharacterLevelReward",
                                levelId=reward.levelId,
                                rewardCollectionId=reward.rewardCollectionId)

        else:
            log.info(f"「{name}」成长值兑换失败")
