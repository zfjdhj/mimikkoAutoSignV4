def task_sign(client, log):
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
