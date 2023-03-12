# 业务逻辑，写web接口
# 7-5 开发 COVID-19 感染数据查询接口 (16:36)

# 7-6 Jinja2 模板渲染前端页面

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
# Jinja2开发，先导入fastapi的模板引擎
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from pydantic import HttpUrl
import requests

from coronavirus import crud, schemas
from coronavirus.database import engine, Base, SessionLocal
from coronavirus.models import City, Data

application = APIRouter()

# Jinja2开发，再创建模板，指定路径
templates = Jinja2Templates(directory="./coronavirus/templates")

# 生成数据库和表
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application.post("/create_city", response_model=schemas.ReadCity)
def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.province)
    if db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City already registered")
    return crud.create_city(db=db, city=city)


@application.get("/get_city/{city}", response_model=schemas.ReadCity)  # 返回类型response_model
def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return db_city # db_city.dict()


@application.get("/get_cities", response_model=List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities


@application.post("/create_data", response_model=schemas.ReadData)
def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
    return data


@application.get("/get_data")
def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return data


def bg_task(url: HttpUrl, db: Session):
    """这里注意一个坑，不要在后台任务的参数中db: Session = Depends(get_db)这样导入依赖"""
    requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    s.trust_env = False

    city_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=false", timeout=500, verify=False)

    if 200 == city_data.status_code:
        db.query(City).delete()  # 同步数据前先清空原有的数据
        for location in city_data.json()["locations"]:
            city = {
                "province": location["province"],
                "country": location["country"],
                "country_code": "CN",
                "country_population": location["country_population"]
            }
            crud.create_city(db=db, city=schemas.CreateCity(**city))

    city_data.close()

    coronavirus_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=true")

    if 200 == coronavirus_data.status_code:
        db.query(Data).delete()
        for city in coronavirus_data.json()["locations"]:
            db_city = crud.get_city_by_name(db=db, name=city["province"])
            for date, confirmed in city["timelines"]["confirmed"]["timeline"].items():
                data = {
                    "date": date.split("T")[0],  # 把'2020-12-31T00:00:00Z' 变成 ‘2020-12-31’
                    "confirmed": confirmed,
                    "deaths": city["timelines"]["deaths"]["timeline"][date],
                    "recovered": 0  # 每个城市每天有多少人痊愈，这种数据没有
                }
                # 这个city_id是city表中的主键ID，不是coronavirus_data数据里的ID
                crud.create_city_data(db=db, data=schemas.CreateData(**data), city_id=db_city.id)
    coronavirus_data.close()


@application.get("/sync_coronavirus_data/jhu")
def sync_coronavirus_data(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """从Johns Hopkins University同步COVID-19数据"""
    background_tasks.add_task(bg_task, "https://coronavirus-tracker-api.herokuapp.com/v2/locations", db)
    return {"message": "正在后台同步数据..."}


# 这种开发方式，前后端不分离
@application.get("/")
def coronavirus(request: Request, city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 若不传城市参数，则返回前100条
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {
        "request": request,  # 第一个是固定的，就这么写
        "data": data,
        "sync_data_url": "/coronavirus/sync_coronavirus_data/jhu"
    })  # 第二个要传入显示在前段的内容，字典格式

