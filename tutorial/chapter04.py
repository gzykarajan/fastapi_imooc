from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union

app04 = APIRouter()

"""Response Model 响应模型"""
"""
场景：
用户登录，输入用户名、手机号、密码
后端返回用户名、手机号，不返回密码
"""


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr  # 用 EmailStr 需要 pip install pydantic[email]
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


# 建2个数据记录
users = {
    "user01": {"username": "user01", "password": "123123", "email": "user01@example.com"},
    "user02": {"username": "user02", "password": "123456", "email": "user02@example.com", "mobile": "110"}
}


@app04.post("/response_model", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """response_model_exclude_unset=True表示默认值不包含在响应中，仅包含实际给的值，如果实际给的值与默认值相同也会包含在响应中"""
    print(user.password)  # password不会被返回
    # return user
    return users["user01"]


@app04.post(
    "/response_model/attributes",
    # response_model=UserOut,
    # response_model=Union[UserIn, UserOut],
    response_model=List[UserOut]  # 列表里的任意格式模型都可以
    # response_model_include=["username", "email"],
    # response_model_exclude=['mobile']
)
async def response_model_attributes(user: UserIn):
    """response_model_include列出需要在返回结果中包含的字段；response_model_exclude列出需要在返回结果中排除的字段"""
    # del user.password  # 删掉密码字段
    # return user
    return [user, user]  # 跟response_model=List[UserOut] 配合使用


"""Response Status Code 响应状态码"""
"""对应from fastapi import status"""


@app04.post("/status_code", status_code=200)
async def status_code():
    return {"status_code": 200}


@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
async def status_attribute():
    return {"status_code": status.HTTP_200_OK}


"""Form Data 表单数据处理"""


@app04.post("/login/")
async def login(username: str = Form(...),
                password: str = Form(...)):
    """用Form类需要pip install python-multipart; Form类的元数据和校验方法类似Body/Query/Path/Cookie"""
    return {"username": username, "password": password}


"""Request Files 单文件、多文件上传及参数详解"""


@app04.post("/file")
async def file_(file: bytes = File(...)):
    """使用File类 文件内容会以bytes的形式读入内存 适合于上传小文件"""
    return {"file_size": len(file)}


@app04.post("/file_list")
async def file_list(file: List[bytes] = File(...)):
    """List[bytes] 于上传多个小文件"""
    return {"file_size": len(file)}


@app04.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    使用UploadFile类的优势:
    1.文件存储在内存中，使用的内存达到阈值后，将被保存在磁盘中
    2.适合于图片、视频大文件
    3.可以获取上传的文件的元数据，如文件名，创建时间等
    4.有文件对象的异步接口
    5.上传的文件是Python文件对象，可以使用write(), read(), seek(), close()操作 经常用
    """
    for file in files:
        contents = await file.read()
        print(contents)
    return {"file_name": files[0].filename, "content_type": files[0].content_type}


"""【见run.py】FastAPI项目的静态文件配置"""

"""Path Operation Configuration 路径操作配置"""


@app04.post(
    "/path_operation_configuration",
    response_model=UserOut,
    # tags=["Path", "Operation", "Configuration"],
    summary="This is summary",
    description="This is description",
    deprecated=True,
    status_code=status.HTTP_200_OK
)
async def path_operation_config(user: UserIn):
    """
    Path Operation Configuration 路径操作配置
    :param user: 用户信息
    :return: 返回结果
    """
    return user.dict()


"""【见run.py】FastAPI 应用的常见配置项"""

"""Handling Errors 错误处理，需导入HTTPException包"""


@app04.get("/http_exception")
async def http_exception(city: str):
    if city != "Beijing":
        raise HTTPException(status_code=404, detail="City is not found",
                            header={"X-Error": "Error"})
    return {"city": city}


@app04.get("/http_exception/{city_id}")
async def override_http_exception(city_id: int):
    if city_id == 1:
        raise HTTPException(status_code=418, detail="Nope there is no 1")  # 返回一个文本！
    return {"city_id": city_id}



