from typing import Annotated

from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


@router.get(
    "/{model_id}",
    summary="Get train model location",
    response_description="Path to trained model",
)
async def get_model(
    model_id: Annotated[int, Path(title="The ID of the model to get")],
    name: Annotated[str, Query(title="Name of the model")],
):
    print(f"GET model_id={model_id} ({type(model_id)}); name={name} ({type(name)})")
    return __file__


class Model(BaseModel):
    model_id: int
    name: str


@router.post(
    "/{model_id}",
    summary="Set train model location",
    response_description="Confirmation of new path to trained model",
)
async def post_model(
    model_id: Annotated[int, Path(title="The ID of the model to get")],
    name: Annotated[str, Query(title="Name of the model")],
    model: Annotated[Model, Body(title="Name and ID of the model")],
):
    print(
        f"POST model_id={model_id} ({type(model_id)}); name={name} ({type(name)}); "
        f"model={model} ({type(model)})"
    )
    return JSONResponse(content={"id": id, "name": name, "model": model})
