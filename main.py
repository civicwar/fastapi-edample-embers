import json
from fastapi import Body, FastAPI

from market.market_models import MarketOutputModel
from market.market_pb2 import MarketInput
from market.market_pb2_grpc import MarketModuleStub

import grpc

from models import MarketModuleInput

app = FastAPI()

# MM MODULE
MM_HOST = "localhost"
MM_PORT = 50054


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.post(
    '/xpto', response_model=MarketOutputModel
)
async def market_test(input_dict: MarketModuleInput = Body()):
    market_channel = grpc.insecure_channel(f"{MM_HOST}:{MM_PORT}")
    market_module = MarketModuleStub(market_channel)

    input_short_term = MarketInput(
        input=json.dumps(input_dict.dict())
    )
    result = market_module.RunShortTermMarketDirect(input_short_term)

    model = MarketOutputModel().from_grpc(result)

    print(model)

    return model
