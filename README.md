# Seckill API Test

秒杀系统接口自动化测试框架 —— pytest + requests + 数据驱动。

被测系统：[seckill](D:\code\seckill)（Spring Boot + MySQL + Redis + RabbitMQ）

## 测试结果

```
16 cases collected
13 passed, 3 xfailed  in 2.14s
```

3 个 `xfail` 是**已复现并由用例锁定**的缺陷，详见 [BUGS.md](BUGS.md)。

## 目录结构

```
seckill-test/
├── api/
│   └── seckill_api.py        # 接口封装层，HTTP 细节收敛在此
├── data/
│   └── seckill_cases.json    # 测试数据（数据驱动）
├── tests/
│   ├── test_seckill.py       # 功能用例 + 已知缺陷用例
│   ├── test_boundary.py      # 边界 / 异常用例
│   ├── test_params.py        # 参数类型校验
│   └── test_concurrency.py   # 并发防超卖用例
├── conftest.py               # fixture：库存重置
├── config.py                 # 基础地址 / 超时
├── pytest.ini                # 标记与默认参数
├── BUGS.md                   # 缺陷清单（含根因与建议）
└── 测试用例设计.md            # 等价类 / 边界值 / 场景法
```

## 快速开始

```bash
pip install -r requirements.txt

# 被测服务需先启动（默认 http://localhost:8081）
pytest

# 只跑冒烟
pytest -m smoke

# 跳过已知缺陷
pytest -m "not bug"

# 生成 HTML 报告
pytest --html=report.html --self-contained-html
```

## 设计要点

**分层**：`api/` 只负责 HTTP，`tests/` 只负责断言，`data/` 只放数据。接口变了改 `api/`，用例不用动。

**数据驱动**：`test_seckill_by_data` 从 JSON 读取参数与期望值，新增场景只需加一行数据。

**状态隔离**：`fresh_stock` fixture 在每条依赖库存的用例前调用 `/admin/reload-stock`，把 Redis 库存重置为 DB 值，避免用例互相污染。

**已知缺陷追踪**：缺陷用 `@pytest.mark.xfail(strict=True, reason="BUG-00x ...")` 标注，套件保持绿色，同时缺陷可被单独筛选：`pytest -m bug -rx`。

## 用例覆盖

| 类型 | 场景 | 数量 |
|---|---|---|
| 功能 | 商品列表、下单成功、remain 递减、响应字段完整 | 6 |
| 数据驱动 | 普通用户 / 另一用户 / 商品不存在 | 3 |
| 边界 | goodsId = 0、-1 | 2 |
| 参数校验 | userId/goodsId 非数字、userId 缺省 | 3 |
| 并发 | 32 线程并发下单，断言成功数 == 库存数 | 1 |
| 缺陷复现 | BUG-001 / 002 / 003 | 3 |

## 发现的缺陷

| ID | 描述 | 严重程度 |
|---|---|---|
| BUG-001 | 不存在的商品返回 200 而非 404 | 中 |
| BUG-002 | 查询不存在的订单返回 200 + 空 body | 中 |
| BUG-003 | 重复下单返回 success:true 但订单未落库 | **高** |

详情见 [BUGS.md](BUGS.md)。

## 环境说明

- Python 3.14（3.10+ 均可）
- 依赖仅 `pytest` + `requests`（测试数据用 JSON 而非 YAML，规避 3.14 无预编译包的问题）

## TODO

- [ ] 接入 allure 报告
- [ ] GitHub Actions：服务容器 + 自动测试
- [ ] 增加安全类用例（SQL 注入、超长参数）
