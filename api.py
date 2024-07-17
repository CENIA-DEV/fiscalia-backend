from fastapi import FastAPI, HTTPException

from src.items import (
    DeleteRequest,
    RucCreateRequest,
    RucRequest,
    RucUpdateRequest,
    UserRequest,
)
from src.postgres import PostgresDB

app = FastAPI()
db = PostgresDB(queries_path="src/queries.json")


@app.get("/get_rucs/")
def get_rucs():
    try:
        result = db.get_rucs()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_user_info/")
def get_user_info(request: UserRequest):
    try:
        result = db.get_user_info(request.user)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_ruc_info/")
def get_ruc_info(request: RucRequest):
    try:
        result = db.get_ruc_info(request.rucs_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_ruc/")
def create_ruc(request: RucCreateRequest):
    try:
        result = db.create_ruc(request.dicc_causa)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete_rucs/")
def delete_rucs(request: DeleteRequest):
    try:
        result = db.delete_rucs(request.rucs_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_ruc/")
def update_ruc(request: RucUpdateRequest):
    try:
        result = db.update_ruc(request.ruc, request.update_dicc)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
