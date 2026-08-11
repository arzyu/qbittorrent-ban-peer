

# qbittorrent-ban-peer

为 qBittorrent 屏蔽吸血客户端

## 运行

* 运行前必须在 qBittorrent 的设置中启用 Web UI 功能，默认账号密码为 `admin` / `password`，如需修改请同步更改 `main.py` 中的配置
* 本项目使用 `pipenv` 管理依赖，请确保已安装 `pipenv`

```shell
cd qbittorrent-ban-peer

# 安装依赖
pipenv install --dev

# 进入 python venv shell 并运行程序
pipenv shell
python ./main.py
```

```
# 运行时每隔 5 秒检查 peer，将吸血客户端 IP 加入到屏蔽列表（qBittorrent 设置 > 链接 > IP 过滤）
$ python ./main.py
# qBittorrent: v4.4.5
# qBittorrent Web API: 2.8.5
>> ban: **.**.**.***:15000 "-XL0012-__%___!!_"
>> ban: ***.***.***.***:10337 "-XL0012-s?_zd__N"
```
