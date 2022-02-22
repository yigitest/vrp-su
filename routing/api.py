from fastapi import FastAPI, HTTPException

from .models import InputData, OutputData, HTTPError
from .ortools_routing import solveOrtoolsRouting
from .settings import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Status OK"}


@app.post(
    "/",
    responses={
        200: {"model": OutputData},
        500: {
            "model": HTTPError,
            "description": "No Solution Found",
        },
    },
)
def task(data: InputData) -> OutputData:
    output_data = solveOrtoolsRouting(data)

    if output_data:
        return output_data
    else:
        raise HTTPException(status_code=500, detail="No Solution Found")
