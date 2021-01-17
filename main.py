from datetime import datetime
from typing import Optional
from typing import List
from typing import Set
from typing import Tuple
from  typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# 参数是包含三个元素的元祖(int, int, str)和包含字节的set,包含str的list
def process_items(items_t: Tuple[int, int, str], items_s: Set[bytes], item_l: List[str]):
    return items_t, items_s, item_l


# 参数为字典，字典的key为str，value为float
def process_item(prices: Dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)


class Person:
    def __init__(self, name: str, age: str):
        self.name = name
        self.age = age


# 参数为Person类型的变量
def get_person_name(person: Person):
    return person.name, person.age


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}

user = User(**external_data)
print(user)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get('/')
def index():
    """首页视图函数"""
    return {'message': 'index'}


# message表示url路径参数是一个字符串，q表示一个查询字符串，默认为None
@app.get('/hello/{message}')
async def hello(message: str, q: Optional[str] = None):
    print(q)
    return {'message': message}


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}