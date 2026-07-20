# 第8天学生项目：Flask数据看板强化

## 运行方法

```bash
python -m pip install -r requirements.txt
python validate_day08_environment.py
python app.py
```

浏览器访问 `http://127.0.0.1:5000`。

- 用户名：`student`
- 密码：`day07`

## 第8天学习目标

本项目承接第7天的电商数据看板。请在原有页面、登录和问答功能基础上，完成新的路由、JSON接口、参数处理、错误响应和测试。

登录后重点测试：`/dashboard`、`/assistant`、`/health`、`/api/metrics`和`/api/categories?category=Fashion`。

## 第8天核心TODO

- `TODO 8-1`：完成`/api/metrics`指标JSON接口；
- `TODO 8-2`：完成`/api/categories`的查询参数筛选；
- `TODO 8-3`：统一400错误JSON结构；
- `TODO 8-4`：检查数据服务返回值可被`jsonify`序列化；
- 为新增接口编写至少3条Flask测试。

## 提交方式

不要新建GitHub仓库。继续使用第7天的课程仓库，在其中新增`day08_flask_upgrade/`目录，或按教师指定的第8天目录提交。提交前运行：

```bash
python validate_day08_environment.py
python validate_day08_submission.py
git status
git add day08_flask_upgrade
git diff --cached
git commit -m "完成第8天Flask项目强化"
git push
```

不要提交`.venv/`、`__pycache__/`、`.env`、真实密钥或其他缓存文件。

## 学生信息

- 姓名：彭豪克
- 学号：24012441
- 已完成路由或接口：  
/health - 健康检查接口（无需登录，返回服务状态）  
/api/metrics - 指标卡数据接口（登录后返回 JSON，含 label/value/note）  
/api/categories - 品类筛选接口（支持 ？category=Fashion 参数，筛选逻辑生效）  
/api/ask - 智能问答接口（POST 请求，返回规则问答结果）  
/login - 登录接口（GET/POST，账号 student/day07）  
/logout - 退出登录  
/dashboard - 数据看板页面（含指标卡、表格、图表）  
/assistant - 智能问答页面
- 测试文件：  
tests/test_api.py - 已编写并全部通过（4 passed）：  
test_health：测试 /health 返回 200  
test_metrics_unauthorized：测试未登录被拦截  
test_metrics_authorized：测试登录后可获取指标数据  
test_categories_filter_fashion：测试品类筛选生效
- 尚未解决的问题：无
