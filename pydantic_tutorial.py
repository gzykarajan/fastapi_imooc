from datetime import datetime, date
from pathlib import Path
from typing import List
from typing import Optional

from pydantic import BaseModel, ValidationError

print("\033[31m1. --- Pydantic的基本用法。Pycharm可以安装Pydantic插件 ---\033[0m")


class User(BaseModel):
    id: int  # 必须字段
    name: str = "John Snow"  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = []   # 列表中元素是int类型或者可以直接转换成int类型


external_data = {
    "id": 123,
    "signup_ts": "2022-12-12 12:22",
    "friends": [1, 2, 3]
}

user = User(**external_data)
"""
说明： 定义函数，参数前加一个 * ，参数会以元组(tuple)的形式导入，
存放所有未命名的变量参数；带2个 *，则表示字典。
"""
print(user.id, user.friends)
print(str(user.signup_ts))
print(user.dict())


print("\033[31m2. --- 校验失败处理 ---\033[0m")
try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, "not number"])
except ValidationError as e:
    print(e.json())

print("\033[31m3. --- 模型类的的属性和方法 ---\033[0m")
print(user.dict())
print(user.json())
print(user.copy())  # 这里是浅拷贝

