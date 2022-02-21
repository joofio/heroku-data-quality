from fastapi import FastAPI
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from enum import Enum
import re
from collections import Counter
import datetime
import math
import json
from typing import List, Optional
import unicodedata
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from enum import Enum
from fastapi import Request


app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Range(BaseModel):
    lower: str
    upper: str

class Output(str,Enum):
    one="Ok"
    two="Warning: Possible Error"
    three="Error: please check value"


class Evaluation(BaseModel):
    range: Range
    output: Output

class Input(BaseModel):
    snomed:str
    value:float
    unit:str

@app.get("/",response_class=HTMLResponse)
async def root(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.post("/CorrectnessCheck",response_model=Evaluation)
async def quality_check(input: Input):
    doc={}
    doc["output"]="Ok"
    doc["range"]={"lower":0,"upper":100}
    return doc

@app.post("/comparabilityCheck",response_model=Evaluation)
async def comparability_check():
    doc={}
    doc["output"]="Ok"
    doc["range"]={"lower":0,"upper":100}
    return doc

@app.post("/comparabilityCheck")
async def completeness_check():
    doc={}
    doc["output"]="Ok"
    doc["range"]={"lower":0,"upper":100}
    return doc