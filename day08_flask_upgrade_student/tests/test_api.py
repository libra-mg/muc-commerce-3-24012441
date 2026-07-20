import pytest
from app import app

@pytest.fixture
def client():
    """创建测试客户端，开启测试模式，自动处理会话 cookie。"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def login(client, username='student', password='day07'):
    """登录辅助函数，返回登录响应。"""
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=False)


def test_health(client):
    """测试 /health 返回 200 及正确 JSON。"""
    rv = client.get('/health')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['ok'] is True
    assert json_data['service'] == 'day08-flask-upgrade'


def test_metrics_unauthorized(client):
    """未登录访问 /api/metrics 应被重定向到登录页。"""
    rv = client.get('/api/metrics')
    assert rv.status_code == 302
    # 检查重定向位置包含 /login
    assert '/login' in rv.headers['Location']


def test_metrics_authorized(client):
    """登录后访问 /api/metrics 返回 200 和正确的指标数据。"""
    # 先登录
    login_rv = login(client)
    assert login_rv.status_code == 302  # 登录成功重定向

    rv = client.get('/api/metrics')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['ok'] is True
    assert 'metrics' in json_data

    metrics = json_data['metrics']
    assert isinstance(metrics, list)
    assert len(metrics) > 0
    # 验证每条指标包含 label, value, note 字段
    for item in metrics:
        assert 'label' in item
        assert 'value' in item
        assert 'note' in item


def test_categories_filter_fashion(client):
    """登录后请求 /api/categories?category=Fashion，验证筛选生效。"""
    # 登录
    login(client)

    rv = client.get('/api/categories?category=Fashion')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['ok'] is True
    assert json_data['category'] == 'Fashion'

    rows = json_data['rows']
    # 确保所有行的偏好品类都是 Fashion
    for row in rows:
        assert row['偏好品类'] == 'Fashion'