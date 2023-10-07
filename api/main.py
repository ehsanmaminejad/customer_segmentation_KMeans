import os
import sys

import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from starlette.responses import FileResponse

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

from startup import run
import etl.extract as extract
from etl.transform import Transform


app = FastAPI()

# Define a Pydantic model for the list of dictionaries
class DataList(BaseModel):
    data : List[dict]

# Create a route that expects a POST request with a JSON body containing a list of dictionaries
@app.post("/customer_data/", status_code=200)
async def customer_data(data_list: DataList):
    # Process the list of dictionaries
    customer_data = data_list
    if customer_data.data:
        try:
            run(customer_data.data)
            return {"message": "Data received and processed successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error:{str(e)}, message: process was unsuccessful")
    else:
        raise HTTPException(status_code=400, detail="No data provided")

@app.get("/")
async def read_index():
    return FileResponse(f'{root_path}/api/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10001)