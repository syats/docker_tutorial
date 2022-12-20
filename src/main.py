from typing import Union
import os.path
import os

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import requests
import json

appname = os.getenv("service_name","no_name_given")
app = FastAPI(title=appname)
basedir = "/data/"


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/reverse_url")
def rev(text_url: str):
    r = requests.get(text_url)
    rj = r.json()
    print("got back\n",json.dumps(rj,indent=1),"\nfrom",text_url)
    text = rj
    return text[::-1]

@app.get("/reverse_text")
def revurl(text: str):
    return {"text": text[::-1]}

@app.post("/write_text/{file_name}")
def put_item(file_name: str,
              text: str = Body(...)):
    fname = os.path.join(basedir, file_name)
    if os.path.isfile(fname):
        return JSONResponse(status_code=409, content={"message":"File already exists"})
    if not os.path.isdir(basedir):
        return JSONResponse(status_code=501, content={"message":"Directory not writeable"})
    with open(fname,"w") as fout:
        fout.write(text)
    return JSONResponse(status_code=201, content={"message":"success",
                                                  "file_name":file_name})
    

@app.get("/read_text")
def read_item(file_name : str = "file.txt"):
    fname = os.path.join(basedir, file_name)
    if not os.path.isfile(fname):
        return JSONResponse(status_code=501, content={"message":"File not Found"})
    with open(fname) as fin:
        text = fin.read()
        return text
