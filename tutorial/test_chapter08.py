# 测试用例
from fastapi.testclient import TestClient

from run import app

"""Testing 测试用例"""

client = TestClient(app)  # pip install pytest


def test_run_bg_task():
    response = client.post(url="/chapter08/background_tasks?framework=FastAPI")
    assert response.status_code == 200
    assert response.json() == {"message": "任务已在后台运行"}


def test_dependency_run_bg_task():
    response = client.post(url="/chapter08/dependency/background_tasks")
    assert response.status_code == 200
    assert response.json() is None


def test_dependency_run_bg_task_q():
    response = client.post(url="/chapter08/dependency/background_tasks?q=a")
    assert response.status_code == 200
    assert response.json() == {"message": "README.md更新成功"}

