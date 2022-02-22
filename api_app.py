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

df=pd.read_csv("data-quality-v1.csv")
class Range(BaseModel):
    lower: str
    upper: str

class Output(str,Enum):
    one="Ok"
    two="Warning: Possible Error"
    three="Error: please check value"

class Columns(str,Enum):
    a_para = "A_PARA"
    a_gesta = "A_GESTA"
    eutocito_anterior = "EUTOCITO_ANTERIOR"
    ventosas_anterior = "VENTOSAS_ANTERIOR"
    forceps_anterior = "FORCEPS_ANTERIOR"
    cesarianas_anterior = "CESARIANAS_ANTERIOR"
    idade_materna = "IDADE_MATERNA"
    peso_inicial = "PESO_INICIAL"
    imc = "IMC"
    numero_consultas_pre_natal = "NUMERO_CONSULTAS_PRE_NATAL"
    idade_gestacional_admissao = "IDADE_GESTACIONAL_ADMISSAO"
    semanas_gestacao_parto = "SEMANAS_GESTACAO_PARTO"
    peso_admissao_internamento = "PESO_ADMISSAO_INTERNAMENTO"
    estimativa_peso_eco_30 = "ESTIMATIVA_PESO_ECO_30"
    estimativa_peso_eco_31 = "ESTIMATIVA_PESO_ECO_31"
    estimativa_peso_eco_32 = "ESTIMATIVA_PESO_ECO_32"
    estimativa_peso_eco_24 = "ESTIMATIVA_PESO_ECO_24"
    estimativa_peso_eco_25 = "ESTIMATIVA_PESO_ECO_25"
    estimativa_peso_eco_26 = "ESTIMATIVA_PESO_ECO_26"
    estimativa_peso_eco_27 = "ESTIMATIVA_PESO_ECO_27"
    estimativa_peso_eco_28 = "ESTIMATIVA_PESO_ECO_28"
    estimativa_peso_eco_29 = "ESTIMATIVA_PESO_ECO_29"
    estimativa_peso_eco_33 = "ESTIMATIVA_PESO_ECO_33"
    estimativa_peso_eco_34 = "ESTIMATIVA_PESO_ECO_34"
    estimativa_peso_eco_35 = "ESTIMATIVA_PESO_ECO_35"
    estimativa_peso_eco_36 = "ESTIMATIVA_PESO_ECO_36"
    estimativa_peso_eco_37 = "ESTIMATIVA_PESO_ECO_37"
    estimativa_peso_eco_38 = "ESTIMATIVA_PESO_ECO_38"
    estimativa_peso_eco_39 = "ESTIMATIVA_PESO_ECO_39"
    estimativa_peso_eco_40 = "ESTIMATIVA_PESO_ECO_40"
    estimativa_peso_eco_41 = "ESTIMATIVA_PESO_ECO_41"
class Evaluation(BaseModel):
    range: Range
    output: Output

class Input(BaseModel):
    snomed:str
    value:float
    unit:str
    column: Columns = Field(
        "IMC", title="Column name to be evaluated", 
    )


def checkoutlier(x,iqr,q1,q3):
    if  pd.isna(x):
        return 0,None,None

    ll_threshold=q1-iqr*3
    uu_threshold=q3+iqr*3
    if x<ll_threshold or x>uu_threshold:
        return 2,ll_threshold,uu_threshold
    l_threshold=q1-iqr*1.5
    u_threshold=q3+iqr*1.5
    if x<l_threshold or x>u_threshold:
        return 1,l_threshold,u_threshold
    return 0,l_threshold,u_threshold
       


@app.get("/",response_class=HTMLResponse)
async def root(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.post("/CorrectnessCheck",response_model=Evaluation)
async def quality_check(input: Input):
    sel=df[df["column"]==input.column]
    print(sel)
    q1=sel["q1"].values[0]
    q3=sel["q3"].values[0]
    iqr=sel["iqr"].values[0]
    print(q1,q3,iqr)
    output,l,u=checkoutlier(input.value,iqr,q1,q3)
    label="Ok"

    if output==1:
        label="Warning: Possible Error"
    if output==2:
        label="Error: please check value"

    doc={}
    doc["output"]=label
    doc["range"]={"lower":l,"upper":u}
    return doc

@app.post("/comparabilityCheck",response_model=Evaluation)
async def comparability_check():
    doc={}
    doc["output"]="Ok"
    doc["range"]={"lower":0,"upper":100}
    return doc

@app.post("/completenessCheck")
async def completeness_check():
    doc={}
    doc["output"]="Ok"
    doc["range"]={"lower":0,"upper":100}
    return doc