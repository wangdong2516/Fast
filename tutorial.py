# 教程
# 1. 运行项目
# uvicorn main:app --reload

from typing import Union, Optional, Set, List
from enum import Enum
from fastapi import FastAPI, Query, Body, File, UploadFile
from fastapi import Cookie
from fastapi import status
from fastapi import  HTTPException
from fastapi import Form
from fastapi import Header
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr
from pydantic import Field
from pydantic import HttpUrl
from fastapi import Request
from starlette.responses import Response, JSONResponse

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get('/files/{file_path: path}')
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get('/db')
async def get_db(page: str, size: int, short: bool = False):
    """
        声明不属于路径参数的其他参数的时候，将会自动解释为查询字符串参数
    :param page:
    :param size:
    :return:
    """
    return {'page': page, 'size': size, 'short': short}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    """
        user_id为必传参数
        item_id为必传参数
        q为类型为str的可选参数，无默认值
        short为类型为bool的可选参数，有默认值
    :param user_id:
    :param item_id:
    :param q:
    :param short:
    :return:
    """
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    """
        Query对象的第一个参数是用来指定默认值的，
        此外可以进行其他的一些操作，比如min_length,max_length, regex， gt, ge, lt,le等
    :param q:
    :return:
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


class Item(BaseModel):
    name: str
    age: int = None
    description: Optional[str] = Field(None, max_length=300)
    price: float
    tax: Optional[float] = None

    # 声明一个示例
    class Config:
        schema_extra = {
            'example': {
                'name': 'wangdong',
                'age': 12,
                'description': 'this is an example',
                'price': 9.99,
                'tax': None,
            }
        }


class User(BaseModel):
    username: str
    full_name: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'username': '用户名',
                'full_name': '完成的名称'
            }
        }

@app.post('/item/{item_id}')
async def create_item(item_id, item: Item):
    """
        声明单个请求体参数，期望的请求体为
        {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2

        }
    :param item_id:
    :param item:
    :return:
    """
    return {'item_id': item_id, 'item': item}


@app.post('/items/{item_id}')
async def update_item(item_id: int, item: Item, user: User):
    """
        声明多个请求体参数，期望的请求体为
        {
             "item": {
                "name": "Foo",
                "description": "The pretender",
                "price": 42.0,
                "tax": 3.2
            },
            "user": {
                "username": "dave",
                "full_name": "Dave Grohl"
            }
        }
        注意区分和单个请求体的区别:
            当有多个请求体的时候，它将使用参数名称作为请求体中的键（字段名称），并期望一个类似于以下内容的请求体
    :param item_id:
    :param item:
    :param user:
    :return:
    """
    return {'item_id': item_id, 'item': item, 'user': user}


@app.post('/items/{item_id}')
async def update_item2(item_id: int, item: Item = Body(..., embed=True)):
    """
        使用Body来指定,期望的请求体为
        {
            "item": {
                "name": "Foo",
                "description": "The pretender",
                "price": 42.0,
                "tax": 3.2
            }
        }
        其中，embed参数指定了item作为key，嵌入到请求体中
    :param item_id:
    :param item:
    :return:
    """
    return {'item_id': item_id, 'item': item}


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item2(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    # 模型之间的嵌套
    image: Optional[Image] = None


@app.put("/items/{item_id}")
async def update_item3(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results


class Item4(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put("/it/{item_id}")
async def update_item4(item_id: int, item: Item4):
    results = {"item_id": item_id, "item": item}
    return results


@app.get("/items/item")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    """
        获取Cookie，使用方式和Query, Path, Body, Field相同
    :param ads_id:
    :return:
    """
    return {"ads_id": ads_id}


@app.get('/cookie')
async def create_cookie(response: Response):
    """
        使用Response对象来设置Cookie
        response.set_cookie(key=key, value=value, expires=3600)
    :param response:
    :return:
    """
    response.set_cookie(key='key', value='value')
    return {'message': 'create cookie success'}


@app.get('/header')
async def get_header(user_agent: Optional[str] = Header(None)):
    """
        获取请求头，使用方式和Cookie相同
        参数的名称就是你想获取的header请求头字段的名称
    :param header:
    :return:
    """
    return {'header': user_agent}


class ResponseItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/response/", response_model=ResponseItem)
async def create_item(item: ResponseItem):
    """
        使用response_model指定响应的模型
        response_model将被用来将输出数据转换为其声明的类型。校验数据。
        响应模型在参数中被声明，而不是作为函数返回类型的注解，这是因为路径函数可能不会真正返回该响应模型，
        而是返回一个 dict、数据库对象或其他模型，然后再使用 response_model 来执行字段约束和序列化。

        response_model指定的是输出(返回的时候使用的模型)
        item参数指定的是输入(请求参数)的模型
    :param item:
    :return:
    """
    print(item)
    return {
        'name': 'wangdong',
        'description': 'this is response',
        'price': "9.99",
        'tax': 0,
        'tags': ['tsr']
    }


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/response_model", response_model=Item, response_model_exclude_unset=True, response_model_exclude_none=True)
async def read_item(item_id: str):
    """
        使用response_model_exclude_unset，返回的响应中将不包括没有被设置的value

        可以使用
            response_model_exclude_defaults=True
            response_model_exclude_none=True
    :param item_id:
    :return:
    """
    return items[item_id]


class Item5(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5


data = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item5,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    """
        response_model_include 和 response_model_exclude参数，接收一个由str组成的set来包含和排除某些属性
        使用set指定，如果使用list或者是tuple指定，将会被转换为set，可以正常工作
    :param item_id:
    :return:
    """
    return data[item_id]


@app.get("/items/{item_id}/public", response_model=Item5, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return data[item_id]


class UserInPut(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOutPut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved



class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


res = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/union", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    """
        Union表示两者中的任意一者
    :param item_id:
    :return:
    """
    return res[item_id]


@app.get('/status_code', status_code=301)
def get_status_code():
    """
        设置响应的状态码
    :return:
    """
    return {'status_code': 201}


@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...)):
    """
        使用Form验证提交的表单数据，同时可以进行校验
    :param username:
    :param password:
    :return:
    """
    return {"username": username}


@app.post('/file')
def upload_file(file: bytes = File(...)):
    """
        上传文件,使用bytes获取上传文件的大小
    :return:
    """
    print(file)
    return {'file_len': len(file)}


@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    """
        获取上传的文件UploadFile
        UploadFile对象的几个属性：
            1. filename:上传文件的文件名
            2. content_type:文件类型
            3. file：类文件对象
        支持的异步方法：
            write(data): 写数据
            read(size): 读数据，单位为字节
            seek(offset):指定偏移量
            close():关闭文件

        可以上传多个文件
    :param file:
    :return:
    """
    print(file)
    await file.read()
    return {'filename': file.filename}


@app.post('/test')
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@app.get('/exception')
async def get_exception(item_id: str):
    """
        抛出异常，添加自定义的头
    headers={"X-Error": "There goes my error"}
    :param item_id:
    :return:
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """
        自定义异常并且注册处理
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.post('/json')
async def get_json(item: Item):
    """
        将数据转换为json，使用jsonable_encoder
    :param item:
    :return:
    """
    print(item)
    print(type(item))
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    print(type(json_compatible_item_data))
    return {'json': json_compatible_item_data}