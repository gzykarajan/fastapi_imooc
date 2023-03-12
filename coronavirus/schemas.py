# 创建好多类
# 对City、Data操作的类
# 7-3 使用 Pydantic 建立与模型类对应的数据格式类 (03:57)

from datetime import date as date_
from datetime import datetime

from pydantic import BaseModel


class CreateData(BaseModel):
    date: date_
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0


class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_population: int


class ReadData(CreateData):
    id: int
    city_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class ReadCity(CreateCity):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
