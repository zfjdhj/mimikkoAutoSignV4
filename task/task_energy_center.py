
import proto.energy_pb2 as energy_pb2


def task_energy_center(client):
    # 任务：能源中心
    if not client.is_login:
        return
    log = client.log
    log.info("「能源中心」任务执行中...")
    # # 获取能源中心仓位信息
    for i in range(2):
        log.info("能源中心check...")
        res = client.call_api(
            "Energy/ListEnergySourceRecord", page=1, pageSize=60)
        for i in res.content:
            status = energy_pb2.Status.Name(i.status)
            if status == 'FINISHED':
                # # # 领取
                client.call_api(
                    "Energy/ReceiveEnergySourceReward", id=i.id)
                log.info(f'能源中心领取{i.position+1}号位')
                continue
            elif status == 'UNLOCKED':
                # # # 创建
                res3 = client.call_api(
                    "Energy/ListEnergySourceModel", page=1, pageSize=60)
                if client.task.EnergyCenter['auto_use_energy_speedup_ticket']:
                    # 判断 电力充能券数量
                    res = client.call_api(
                        "Scalar/GetUserMaterialScalar",
                        scalarCode="_scalar_material_amount",
                        materialCode="energy_speedup_ticket")
                    source_mode = '超级芯片' if res.integerValue > 0 else "普通芯片"
                    log.debug(f"电力充能券：{res.integerValue}")
                else:
                    source_mode = '普通芯片'
                for item in res3.content:
                    if item.name == source_mode:
                        # ## 创建充能
                        client.call_api(
                            "Energy/CreateEnergySourceRecord",
                            modelId=item.modelId, position=i.position)
                        log.info(f'能源中心创建充能{i.position+1}号位({source_mode})')
                continue
    else:
        log.info("能源中心暂时没有事情做")
