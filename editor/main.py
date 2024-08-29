from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse,Response
import json
import cjfile
import os

app = FastAPI()

@app.get("/")
async def webui():
    return HTMLResponse(open("index.html",encoding="utf-8").read())

@app.get("/{file}")
async def file(file:str):
    try:
        return FileResponse(file)
    except:
        return Response(status_code=404)

@app.get("/resource/{file}")
async def file(file:str):
    try:
        return FileResponse(f"resource/{file}")
    except:
        return Response(status_code=404)

@app.post("/save")
async def save(jsn):
    try:
        data = json.loads(jsn)
        print(data)
        if not os.path.isdir(data["path"]):
            os.mkdir(data["path"])
        try:
            print(0)
            with open(f"{data['path']}/question.cjf","w",encoding="UTF-8") as q:
                cjfile.dumpcjf(data['question'],q)
            print(1)
            with open(f"{data['path']}/tests.cjt","w",encoding="UTF-8") as q:
                new = []
                for i in data['tests']:
                    new.append(tuple(i))
                cjfile.dumpcjt(data['tests'],q)
            print(2)
            print("suuccess")
            return True
        except:
            print("failed, read")
            return False
    except:
        print("failed")
        return False
    
@app.post("/getFolder")
async def get_folder(path):
    if os.path.isdir(path):
        result = {}
        with open(f"{path}/question.cjf","r",encoding="utf-8") as f:
            result["question"] = cjfile.loadcjf(f)
        with open(f"{path}/tests.cjt","r",encoding="utf-8") as t:
            result["tests"] = list(map(list,cjfile.loadcjt(t)))
        return json.dumps(result)
    else:
        return False
    
@app.post("/pack")
async def pack(path):
    if os.path.isdir(path):
        try:
            cjfile.packcjz(path)
            return True
        except:
            return False
    else:
        return False