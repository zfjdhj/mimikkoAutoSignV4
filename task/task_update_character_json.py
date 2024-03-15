import json


def task_update_character_json(client):
    # 任务：更新助手列表
    if not client.is_login:
        return
    log = client.log
    log.info("「助手列表」更新中...")
    path = './助手列表.json'
    old_data = get_character_json(path, log)
    new_character_data = get_new_character(client, old_data, path, log)
    if new_character_data:
        log.info(f'新助手：{new_character_data}')
        write_character_json(old_data, new_character_data, path)
    else:
        log.info("暂时没有更新新的助手")


def get_character_json(path, log):
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


def get_new_character(client, data, path, log):
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
