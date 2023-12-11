# mimikkoAutoSignV4  
用于兽耳桌面相关V4接口测试  
不要到处宣传 偷偷用就行了 应该不会封号吧
## 使用
1. 抓包软件获取登录时的`device-id`,`authorization`  
2. 修改`config.yaml`相关设置  
    当前已支持功能  
    |Task|功能|参数|说明|
    |-|-|-|-|
    |Sign|每日签到|`character_code`见下表|日常签到，希望不要断连签|
    |EnergyExchange|成长值兑换|`character_code`见下表|包含助手升级以及领取奖励|
    |EnergyCenter|能源中心|-|默认硬币换电力|  
    |OrdinaryWork|工会悬赏任务|`work_characters`见下表|电力换硬币，积累公会等级|  
    |Task|每日任务|`task_characters`见下表|完成任务获得成长值|
    |MailReceive|邮件领取|-|邮件奖励一键领取|
    |CoinMall|硬币商店|`material_code`见下表|硬币换取每周刷新物品|
    

    | 助手名称 | code |
    | - | - |
    | 诺诺纳 | nonona | 
    | 优莉卡 | ulrica | 
    | 梦梦奈 | momona | 
    | 琉璃 | ruri | 
    | 爱莉安娜 | ariana | 
    | 阿尔法零 | alpha0 | 
    | 卡斯塔莉娅 | kasutaria | 
    | 卡斯塔莉莉 | castariri | 
    | 奈姆利 | nemuri | 
    | 胡桃 | kurumi | 
    | 羲和 | giwa |         
    | 摩耶 | maya | 
    | 苏纳 | suna | 
    | 米璐库 | miruku |         
    | 米露可 | miruku2 | 
    | 食蜂操祈 | shokuhou_misaki | 
    | 御坂妹妹 | sisters | 
    | 中野一花 | nakanoichika | 
    | 中野二乃 | nakanonino | 
    | 中野三玖 | nakanomiku | 
    | 中野四叶 | nakanoyotsuba | 
    | 中野五月 | nakanoitsuki | 
    | 御坂美琴 | misakamikoto | 
    | 白井黑子 | shiraikuroko | 
    | 托尔 | tooru | 
    | 康娜 | kanna | 
    | 阿波连玲奈 | reina | 
    | 环古达 | tamakikotatsu | 
    | 爱丽丝 | alice | 
    | 泠鸢 | yousa | 

    |物品|material_code|
    | :- | :- |
    |补签卡|`_supplementary_signature_card`|
    |工作刷新券|`_work_refresh_ticket`|
    |电力充能券|`energy_speedup_ticket`|
    
3. ```python main.py```
## 说明
这只是一个脚本，不要期望有太多功能。