from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

@app.get("/component/{component_id}")
async def hello_word(component_id: int):
	return {"component_id": component_id}


@app.get("/component/")
async def grp(name: str, age: int):
               nom_c= name + "anderson",
               age_c= age - 3
       	       return {"nom_c": nom_c, "age_c": age_c}



class Coord(BaseModel):
    nom: str
    age: int
    origine: Optional[str]

@app.post("/Model/{id}")
def model(id: int, coord: Coord):
    return {"id": id, "coord": coord.dict()}


class Todo(BaseModel):
       nom: str
       prenom: str
       age: int
       adress: Optional[str]= None 

store_todo = []


@app.get("/get_Todo/")
def get_All_Todo():
    return{"todo": store_todo}


@app.get("/get_Todo/{id}")
def get_Todo_ById(id: int):
    try:
       return store_todo[id]
    except IndexError:
       raise HTTPException (status_code= 404, detail= "todo non trouver")


@app.post("/post_Todo/")
def created_todo(todo: Todo):
    store_todo.append(todo.dict())
    return todo


@app.put("/put_todo/{id}")
def modify_todo(id: int, new_todo: Todo):
    try:
       store_todo[id] = new_todo.dict()
       return store_todo[id]
    except IndexError:
       raise HTTPException (status_code= 404, detail= "todo non trouver")


@app.delete("/delete_todo/{id}")
def supprimer_todo(id: int):
    try:
       obj = store_todo[id]
       store_todo.pop(id)
       return obj
    except IndexError:
       raise HTTPException (status_code= 404, detail= "todo non trouver")


