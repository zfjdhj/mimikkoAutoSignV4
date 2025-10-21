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
    |Task|助手任务|`task_characters`见下表|完成任务获得成长值|
    |MailReceive|邮件领取|-|邮件奖励一键领取|
    |CoinMall|硬币商店|-|硬币换取每周刷新|
    |ActivitySign|活动签到|-|活动签到|
    |UpdateCharacterJson|助手更新|-|更新`助手列表.json`，务必启用|
    |Travel|助手出游|`travel_characters`见下表|旅行收集纪念品|
    
    
    | 助手名称 | code |
    | - | - |
    | 诺诺纳 | character_nonona | 
    | 优莉卡 | character_ulrica | 
    | 梦梦奈 | character_momona | 
    | 琉璃 | character_ruri | 
    | 爱莉安娜 | character_ariana | 
    | 阿尔法零 | character_alpha0 | 
    | 卡斯塔莉娅 | character_kasutaria | 
    | 卡斯塔莉莉 | character_castariri | 
    | 奈姆利 | character_nemuri | 
    | 胡桃 | character_kurumi | 
    | 羲和 | character_giwa |         
    | 摩耶 | character_maya | 
    | 苏纳 | character_suna | 
    | 米璐库 | character_miruku |         
    | 米露可 | character_miruku2 | 
    | 食蜂操祈 | character_shokuhou_misaki | 
    | 御坂妹妹 | character_sisters | 
    | 中野一花 | character_nakanoichika | 
    | 中野二乃 | character_nakanonino | 
    | 中野三玖 | character_nakanomiku | 
    | 中野四叶 | character_nakanoyotsuba | 
    | 中野五月 | character_nakanoitsuki | 
    | 御坂美琴 | character_misakamikoto | 
    | 白井黑子 | character_shiraikuroko | 
    | 托尔 | character_tooru | 
    | 康娜 | character_kanna | 
    | 阿波连玲奈 | character_reina | 
    | 环古达 | character_tamakikotatsu | 
    | 爱丽丝 | character_alice | 
    | 泠鸢 | character_yousa | 
    | 梅莉 | character_melly |
    | 衿 | character_eri |
    | 逢坂大河 | character_aisaka_taiga |
    | 薇尔莉特 | character_violet |
    | 可洛蒂娅 | character_gurodia |
    | 清 | character_kiyo |
    | 一之濑千鹤 | character_mizuhara_chizuru |
    | 更科瑠夏 | character_sarashina_ruka |
    | 樱泽墨 | character_sakurasawa_sumi |
    | 七海麻美 | character_asami_nanami |

    |物品|material_code|
    | :- | :- |
    |补签卡|`_supplementary_signature_card`|
    |工作刷新券|`_work_refresh_ticket`|
    |电力充能券|`energy_speedup_ticket`|
    |硬币兑换九周年限时时光旅票|`coin_to_travel_time_invitation_time_limit_9th`|
    |硬币兑换九周年限时能源罐|`coin_to_energy_pack_s_9th`|
    |硬币兑换九周年限时硬币包小|`coin_to_coin_pack_s_9th`|

    |可支持操作|then_do_task|
    | :- | :- |
    |从头开始执行一遍|task_start|
    |每日签到|task_sign|
    |成长值兑换|task_energy_exchange|
    |能源中心|task_energy_center|
    |工会悬赏任务|task_ordinary_work|
    |助手任务|task_task|
    |邮件领取|task_mail_receive|
    |硬币商店|task_coin_mall|
    |活动签到|task_activity_sign|
    |助手更新|task_update_character_json|
    |助手出游|task_travel|
    
    
3. ```python main.py```
## 说明
这只是一个脚本，不要期望有太多功能。  
## 更新
20250321:(`config.yaml`有变动注意修改。)
- 9周年活动相关内容添加
- 升级app版本4.2.8.2(config.yaml中mimikko_version: "40215")
- Travel(助手出游): add 大洋洲相关内容
- CoinMall(硬币商店): add 额外换取9周年活动添加物品
- 助手列表更新

20240419:
- fix bug: 等待300s,连接超时
- CoinMall(硬币商店):add 高级物资调换券兑换复刻服装，贵重物品开启需谨慎
- CoinMall(硬币商店):del 过期物品兑换项
- `config.yaml`有变动注意修改，为避免错误操作 按需启用各功能

20240407: 
- update: config_example.yaml中错误的默认操作(then_do_task)
    [line:65]OrdinaryWork错误的指向了task_travel
- update: readme.md 新增"可支持操作(then_do_task)"解释字段

20240406：
- fix bug：log文件夹创建错误[#8](https://github.com/zfjdhj/mimikkoAutoSignV4/issues/8)
- OrdinaryWork(公会悬赏),Task(助手任务),Travel(助手出游)：add 等待300秒即将完成的任务
(防止由于网络延时，致使任务完成延后至下一脚本循环，浪费时间收益)
- OrdinaryWork(公会悬赏),Task(助手任务),Travel(助手出游)：add 等待时间完成后执行操作
(用于完成一些自定义操作)

    例如：一个助手同时处于“公会悬赏”，“助手任务”，“助手出游”名单中
    ，即config文件，work_characters，task_characters，travel_characters中  
    默认情况下：等待300s完成任务“助手出游”，仍会安排“助手出游”  
    自定义：`then_do_task: task_ordinary_work`后，待300s后会安排“公会悬赏”。  
    即目前助手优先级：大时间循环下参考config中task先后顺序，等待300s时参考`then_do_task`

- `config.yaml`有变动注意修改，为避免错误操作 按需启用各功能

20240331：
- fix bug：Travel:'ExchangePostcard'
- fix bug：Travel:移动下一区域

20240322：
- CoinMall(硬币商店): add 额外换取活动添加物品
- fix bug

20240320：
- EnergyCenter(能源中心)：add 自动使用电力充能券
- OrdinaryWork(公会悬赏)：add 自动使用工作刷新券
- OrdinaryWork(公会悬赏)：add 优先完成低等级耗时少的任务
- Travel(助手出游): add 旅行区域满人跳转下一区域
- Travel(助手出游): add 明信片兑换

- Travel(助手出游): add 自行添加助手指定区域出游  


