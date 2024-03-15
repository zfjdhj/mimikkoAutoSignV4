def task_mail_receive(client):
    # 任务：邮件一键领取
    if not client.is_login:
        return
    log = client.log
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
