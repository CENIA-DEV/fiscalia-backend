import json

from fastapi import FastAPI, HTTPException

from src.items import RucRequest, RucSearchRequest, RucUpdateRequest
from src.postgres import PostgresDB

app = FastAPI()
db = PostgresDB(queries_path="src/dicts/queries.json")


@app.get("/get_rucs/")
def get_rucs():
    try:
        result = db.get_rucs()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_estados/")
def get_estados():
    return {"estados": ["Sin preclasificar", "Guardado", "Preclasificado"]}


@app.get("/get_grupo_delitos/")
def get_grupo_delitos():
    with open("src/dicts/agrupador.json", "r") as file:
        data = json.load(file)

    agrupadores = []

    for codigo in data.keys():
        agrupador = data[codigo]["agrupador"]
        agrupadores.append(agrupador)

    agrupadores = list(set(agrupadores))

    return {"grupos_delitos": agrupadores}


@app.get("/get_curso_precla/")
def get_curso_precla():
    with open("src/dicts/preclasificacion.json", "r") as file:
        data = json.load(file)

    return data


@app.get("/get_causas/")
def get_causas():
    try:
        rucs_list = db.get_rucs()["rucs_list"]
        result = db.get_ruc_info(rucs_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search_rucs/")
def search_rucs(request: RucSearchRequest):
    provided_fields = request.model_dump(exclude_unset=True)
    search_results = db.search_rucs(provided_fields)

    return search_results


@app.post("/get_ruc_info/")
def get_ruc_info(request: RucRequest):
    try:
        result = db.get_ruc_info(request.rucs_list)
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
