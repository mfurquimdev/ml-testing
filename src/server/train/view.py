from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Path
from fastapi import Query
from pydantic import BaseModel
from pydantic import Field

router = APIRouter()


class Model(BaseModel):
    name: str = Field(title="Name of the model", repr=True)
    num: int = Field(title="ID of the model", repr=True)


@router.post(
    "",
    summary="Request model training Set train model location",
    response_description="Confirmation of new path to trained model",
)
async def post_model(
    num: Annotated[int, Query(title="The ID of the model to get")],
    name: Annotated[str, Query(title="Name of the model")],
    model: Annotated[Model, Body(title="Name and ID of the model")],
):
    print(
        f"POST num={num} ({type(num)}); name={name} ({type(name)}); "
        f"model={model} ({type(model)})"
    )
    return {
        "num": num,
        "name": name,
        "model": model,
    }
