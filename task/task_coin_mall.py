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
                buy_item(
                    client,
                    exchange.target.materialCode,
                    exchange.target.materialName,
                    times)
                log.info(f"硬币换取{times}次{exchange.target.materialName}")
        elif exchange.relationCode in client.task.CoinMall[
                'exchange_list']:
            times = exchange.maxTimes - exchange.userTimes
            log.debug(f"本周还可换取{times}次{exchange.target.materialName}")
            if exchange.maxTimes > exchange.userTimes:
                # # 兑换
                buy_item(
                    client,
                    exchange.target.materialCode,
                    exchange.target.materialName,
                    times,
                    relation_code=exchange.relationCode)
                log.info(f"硬币换取{times}次{exchange.target.materialName}")
    if client.task.CoinMall['clothes_exchange']:
        clothes_exchange(client)


def clothes_exchange(client):
    log = client.log
    # 获取服装兑换列表
    mall_list = client.call_api(
        "Scalar/ListMallExchangeRelation", scope=16, page=1, pageSize=60)
    for clothes in mall_list.content:
        if clothes.canExchangeTimes:
            log.info(f"尚未兑换服装「{clothes.target.materialName}」")
            log.info(
                f"兑换需要:{clothes.source.materialName}*{clothes.source.intValue}")
            if clothes.source.intValue < clothes.source.intUserValue:
                log.info(
                    f"背包拥有数量{clothes.source.intUserValue}，不足以兑换服装")
                return
            else:
                # 兑换
                log.info(f"「{clothes.target.materialName}」兑换中...")
                client.call_api("Scalar/Exchange",
                                relationCode=clothes.relationCode,
                                relationType=clothes.relationType,
                                times=1)
