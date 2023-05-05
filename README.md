# mimikkoAutoSignV4  
用于兽耳桌面相关V4接口测试

## 使用
1. 抓包软件获取登录时的`device-id`,`authorization`  
2. 修改`config.yaml`相关设置  
    当前已支持功能  
    |Task|功能|参数备注|
    |-|-|-|
    |Sign|每日签到|`character_code`见下表|
    |EnergyExchange|成长值兑换|`character_code`见下表|
    |EnergyCenter|能源中心|硬币换电力|  

    | 助手名称 | code |
    | :- | :- |
    | 魔女日记 | nononabook |
    | 诺诺纳 | nonona |
    | 梦梦奈 | momona |
    | 爱莉安娜 | ariana |
    | 米璐库 | miruku |
    | 奈姆利 | nemuri |
    | 琉璃 | ruri |
    | 阿尔法零 | alpha0 |
    | 米露可 | miruku2 |
    | 优莉卡 | ulrica |
3. ```python main.py```
## 说明
这只是一个脚本，不要期望有太多功能。