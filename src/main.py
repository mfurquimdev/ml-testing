import httpx
import multipart  # python_multipart
import numpy as np
import pandas as pd
import scipy
import sklearn
import uvicorn
from fastapi import FastAPI

from train import router as train_router

app = FastAPI()

app.include_router(train_router, prefix="/train", tags=["train"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
