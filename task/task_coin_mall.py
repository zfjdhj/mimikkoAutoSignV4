from task.task_travel import buy_item


def task_coin_mall(client):
    # 任务：硬币商店
    if not client.is_login:
        return
    log = client.log
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
