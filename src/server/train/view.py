from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Path
from fastapi import Query
from pydantic import BaseModel
from pydantic import Field

router = APIRouter()


@router.get(
    "/{num}",
    summary="Get train model location",
    response_description="Path to trained model",
)
async def get_model(
    num: Annotated[int, Path(title="The ID of the model to get")],
    name: Annotated[str, Query(title="Name of the model")],
):
    print(f"GET num={num} ({type(num)}); name={name} ({type(name)})")
    return __file__


class Model(BaseModel):
    name: str = Field(title="Name of the model", repr=True)
    num: int = Field(title="ID of the model", repr=True)


@router.post(
    "/{num}",
    summary="Set train model location",
    response_description="Confirmation of new path to trained model",
)
async def post_model(
    num: Annotated[int, Path(title="The ID of the model to get")],
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
