def task_activity_sign(client):
    # 任务：活动签到
    if not client.is_login:
        return
    log = client.log
    log.info("「活动签到」任务执行中...")
    # 获取活动 id
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
