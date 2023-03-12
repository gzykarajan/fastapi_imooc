import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# 改写HTTPException，需要在主程序中编写
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse # 文本方式返回错误
# from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi.middleware.cors import CORSMiddleware
import time
from apscheduler.schedulers.background import BackgroundScheduler
from tutorial import app03, app04, app05, app06, app07, app08
from coronavirus import application

# app = FastAPI()
app = FastAPI(
    title='FastAPI tutorial',
    description='FastAPI教程',
    version='1.0.0',
    docs_url='/docs',
    # dependencies=[Depends(verify_token), Depends(verify_key)]]
)

# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')
# 大坑：.mount()不要在分路由APIRouter().mount()调用，模板会报错


# @app.exception_handler(StarletteHTTPException)  # 重写HTTPException异常处理器
# async def http_exception_handler(request, exc):
#     """
#
#     :param request: 这个参数不能省！
#     :param exc:
#     :return:
#     """
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.exception_handler(RequestValidationError)  # 重写请求验证异常处理
# async def validation_exception_handler(request, exc):
#     """
#     :param request: 这个参数不能省！
#     :param exc:
#     :return:
#     """
#     return PlainTextResponse(str(exc), status_code=400)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 使用通配符允许所以
    allow_headers=["*"]
)


app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 安全、认证和授权'])
app.include_router(app07, prefix='/chapter07', tags=['第七章 FastAPI的数据库操作和多应用的目录结构设计'])
app.include_router(app08, prefix='/chapter08', tags=['第八章 中间件、CORS、后台任务、测试用例'])
app.include_router(application, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])

# 时间调度测试
# 注释掉这段中间件代码，程序也可以正常跑
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# test_list = ["1"]*10
#
# def check_list_len():
#     global test_list  # you really don't need this either, since you're not reassigning the variable
#     print(f"check_list_len：{len(test_list)}")
#
# @app.on_event('startup')
# def init_data():
#     scheduler = BackgroundScheduler(timezone='Asia/Shanghai')  # 不加时区，会有警告
#     scheduler.add_job(check_list_len, 'cron', second='*/5')
#     scheduler.start()
#
# @app.get("/pop")
# async def list_pop():
#     global test_list
#     test_list.pop(1)
#     return {"test_list": f"current_list_len:{len(test_list)}"}
# 时间调度测试

# 启动命令：uvicorn hello_world:app --reload
if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0',
                port=8000, reload=True,
                debug=True, workers=1)

