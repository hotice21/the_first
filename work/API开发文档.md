此项目用于管理hub中的device信息，分为7个接口。
### 此接口用于获取device的详细信息
| 信息 | 详情 |
| --- | --- |
| 接口地址 | /list |
| 请求方法 | GET |
| 认证需求 | 无 |
| 响应格式 | string |

### 此接口用于获取hub中device的总个数
| 信息 | 详情 |
| --- | --- |
| 接口地址 | /total_amount |
| 请求方法 | GET |
| 认证需求 | 无 |
| 响应格式 | string |

### 此接口用于获取device的名字和对应的开关状态
| 信息 | 详情 |
| --- | --- |
| 接口地址 | /display_status |
| 请求方法 | GET |
| 认证需求 | 无 |
| 响应格式 | string |

### 此接口用于操作device的开启状态
| 信息 | 详情 |
| --- | --- |
| 接口地址 | /execute |
| 请求方法 | GET |
| 认证需求 | 无 |
| 响应格式 | string |

### 此接口用于添加device，需要接收JSON文件及其对应格式
| 信息 | 详情 |
| --- | --- |
| 接口地址 | /add |
| 请求方法 | POST |
| 认证需求 | 无 |
| 响应格式 | string |

JSON文件，hub中的内容依据设备的名称进行改变
`JSON`

```js
{  "hub":
       [
        {
          "device":"#the given device name",
          "name":"#the device name you set",
          "id":"#the unique id in hub",
          "energy_usage": #int,
          ...
        }，
        { ... }
       ]
}
```
设备名称及其需要额外添加的变量
| 设备名称 | 所需变量 |  类型 |
| --- | --- | --- |
| Light | brightness | string|
|Camera|resolution|string|
||angle|int|
|Thermostat|temperature|int|
|  Fridge  | low_temperature | int|
||high_temperature| int |
||stage_status|dict[int]:int|

*Fridge中的stage_status表示 层数 ： 对应的温度（至少有一个）



### 此接口用于移除device，需要接受JSON文件并验证
| 信息 | 详情 |
| --- | --- |
| 接口地址 | /remove |
| 请求方法 | POST |
| 认证需求 | JSON 中 “password”键的值 |
| 响应格式 | string |

只需添加hub中存在的id
`JSON`
```js
{
    "password":"114514",
    "id":[
        "#device_id_1",
        "#device_id_2",
        "#device_id_3"
        ]
}
```
### 此接口用于获取总功耗
| 信息 | 详情 |
| --- | --- |
| 接口地址 |  /total_energy_usage|
| 请求方法 | GET |
| 认证需求 | 无 |
| 响应格式 | string |
### 此接口用于载入定时开关设备数据
| 信息 | 详情 |
| --- | --- |
| 接口地址 |  /schedule|
| 请求方法 | POST |
| 认证需求 | 无 |
| 响应格式 | string |
`JSON`
```js
{
    "%H:%M":{"#id":"on"},
    ...
}
```
* 需要接收JSON文件，覆盖原有设置