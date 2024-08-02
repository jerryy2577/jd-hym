# JD 自用

## 本地使用

- `git clone https://github.com/jerryy2577/jd-hym.git`
- `cp .env.example .env`, 根据实际情况修改.env配置。
- `python jd_wyw_exchange.py` 


## 青龙使用
- 名称: `jd-hym`
- 链接: `https://github.com/jerryy2577/jd-hym.git`
- 分支: `main`
- 定时规则: `0 10 * * *`
- 白名单: `jd_`
- 黑名单: 
- 依赖: `utils|conf|storage|.env|httpx|python-dotenv|redisbloom|telethon`
- 文件后缀: 
- 执行前:
- 执行后:
```sh
if [ ! -f .env ]; then
  cp .env.example .env
fi
```

**拉库完成后, 在库的根目录有个.env文件, 根据注释自行修改配置**