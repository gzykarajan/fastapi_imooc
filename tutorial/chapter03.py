#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__gzy__'

from fastapi import APIRouter, Path, Query, Cookie, Header
from enum import Enum
from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

# Path 路径参数校验的类

app03 = APIRouter()

"""路径参数和数字验证"""

# 函数的顺序就是路由的顺序
@app03.get("/path/parameters")
def path_parameters01():
    return {"message": "This is a message"}


@app03.get("/path/{parameters}")
def path_parameters01(parameters: str):
    return {"message": parameters}


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get("/enum/{city}")  # 枚举类型的参数
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 1492, "death": 7}
    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 971, "death": 9}
    return {"city_name": city, "latest": "unknown"}


# 可以打印路径中的/ \\
@app03.get("/files/{file_path: path}")  # 通过path parameters传递文件路径
def filepath(file_path: str):
    return f"file path is {file_path}"  # f-string


# 路径参数校验
@app03.get("/path_/{num}")
def path_params_validate(
        num: int = Path(..., title="Your number", description="不可描述", ge=1, le=10)
):
    return num


"""Query Parameters and String Validations 查询参数和字符串验证"""
@app03.get("/query")
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/conversion")
def type_conversion(param: bool = False):
    return param


# 字符串校验
@app03.get("/query/validations")
def query_params_validate(
    value: str = Query(..., min_length=9, max_length=16, regex="^a"),  # ...换成None就变成选填的参数
    values: List[str] = Query(default=["v1", "v2"], alias="alias_name")
):
    return value, values


"""Request Body and Fields 请求体和字段"""


class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing")
    country: str
    country_code: str = None
    country_population: int = Field(default=800, title="人口数量",
                                    description="国家的人口数量", ge=800)
    # 定义一个子类

    class Config:
        schema_extra = {
            "example": {
                "name": "Shanghai",
                "country": "China",
                "country_code": "CN",
                "country_population": 1400000000,
            }
        }


@app03.post("/request_body/city")
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


"""Request Body + Path parameters + Query parameters 多参数混合"""


@app03.put("/request_body/city/{name}")
def mix_city_info(
    name: str,  # 就是{name}
    city01: CityInfo,
    city02: CityInfo,
    confirmed: int = Query(ge=0, description="确诊数", default=0),
    death: int = Query(ge=0, description="死亡数", default=0)
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(), city02.dict()


"""Request Body - Nested Models 数据格式嵌套的请求体"""


class Data(BaseModel):
    city: List[CityInfo] = None
    date: date  # 额外的数据类型，还有uuid datetime bytes frozenset等，参考：https://fastapi.tiangolo.com/tutorial/extra-data-types/
    confirmed: int = Field(ge=0, description="确诊数", default=0)
    deaths: int = Field(ge=0, description="死亡数", default=0)
    recovered: int = Field(ge=0, description="痊愈数", default=0)


@app03.put("/request_body/nested")
def nested_models(data: Data):
    return data


"""Cookie 和 Header 参数"""
# 请求头自动转化的功能
@app03.get("/cookie")
def cookie(cookie_id: Optional[str] = Cookie(None)):
    return {"cookie_id": cookie_id}


@app03.get("/header")
def header(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
    """
    有些HTTP代理和服务器是不允许在请求头中带有下划线的，所以Header提供convert_underscores属性让设置
    :param user_agent: convert_underscores=True 会把 user_agent 变成 user-agent
    :param x_token: x_token是包含多个值的列表
    :return:
    """
    return {"user_agent": user_agent, "x_token":x_token}