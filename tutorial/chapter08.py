#!/usr/bin/python3
# -*- coding:utf-8 -*-
from fastapi import APIRouter, BackgroundTasks, Depends
from typing import Optional

app08 = APIRouter()


"""Background Tasks 后台任务"""


# 假设，该函数非常耗时
def bg_task(framework: str):
    with open("README.md", mode="a") as f:
        f.write(f"## {framework} 框架精讲")


@app08.post("/background_tasks")
async def run_bg_task(framework: str, backgroud_task: BackgroundTasks):
    """
    :param framework: 被调用的后台任务函数的参数
    :param backgroud_task: FastAPI.BackgroundTasks
    :return:
    """
    backgroud_task.add_task(bg_task, framework)
    return {"message": "任务已在后台运行"}


def continue_write_readme(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        background_tasks.add_task(bg_task, "\n> 整体的介绍 FastAPI，快速上手开发，结合 API 交互文档逐个讲解核心模块的使用\n")
    return q


@app08.post("/dependency/background_tasks")
async def dependency_run_bg_task(q: str = Depends(continue_write_readme)):
    if q:
        return {"message": "README.md更新成功"}

