
from typing import Union

from fastapi import FastAPI, Path, Depends
from app.utils.base import api_request
from pydantic import BaseModel, Field
from enum import Enum
# New Imports for main.py
from fastapi.security.api_key import APIKey
from app.utils import auth

app = FastAPI()

class SideEnum(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class TypeEnum(str, Enum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'


class CreateOrder(BaseModel):
    symbol: str = Field(..., description='Par a operar')
    side: SideEnum = Field(..., description='Compra o Venta')
    type: TypeEnum = Field(..., description='Indica si es orden a mercado o limite')
    amount: float = Field(..., description='Monto a operar')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/common_symbol/{symbol}")
def common_symbol(
    symbol: str = Path(description='Simbolo a consultar', default='BTC-USDT'),
    api_key: APIKey = Depends(auth.get_api_key)
):
    response = api_request(
        '/openApi/spot/v1/common/symbols',
        method='GET',
        query_params=f'symbol={symbol}'
    )
    return response

@app.get("/balance")
def balance():
    response = api_request(
        '/openApi/spot/v1/account/balance',
        method='GET',
    )
    return response


@app.post("/create_order")
def create_order(item: CreateOrder):
    """
        Servicio para realizar una orden
    """
    query_params = f'symbol={item.symbol}&side={item.side.value}&type={item.type.value}'

    if item.side.value == 'BUY':
        query_params += f'&quoteOrderQty={item.amount}'
    else:
        query_params += f'&quantity={item.amount}'

    response = api_request(
        '/openApi/spot/v1/trade/order',
        method='POST',
        query_params=query_params
    )
    return response