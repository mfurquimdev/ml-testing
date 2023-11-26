import httpx
import multipart  # python_multipart
import numpy as np
import pandas as pd
import scipy
import sklearn
import uvicorn
from fastapi import FastAPI
from sample import router as sample_router

from config import backend_settings

app = FastAPI()

app.include_router(sample_router, prefix="/sample", tags=["sample"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=backend_settings.port_number)
