from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.utils import authorize
from src import ModelSchema

router = APIRouter()


# In-memory storage for demonstration purposes
models_db = []


@router.post("/models", response_model=ModelSchema, status_code=201)
async def create_model(model: ModelSchema, _=Depends(authorize)):
    model.id = len(models_db) + 1
    models_db.append(model)
    return model


@router.get("/models", response_model=List[ModelSchema])
async def read_models(_=Depends(authorize)):
    return models_db


@router.get("/models/{model_id}", response_model=ModelSchema)
async def read_model(model_id: int, _=Depends(authorize)):
    for model in models_db:
        if model.id == model_id:
            return model
    raise HTTPException(status_code=404, detail="Model not found")


@router.put("/models/{model_id}", response_model=ModelSchema)
async def update_model(model_id: int, updated_model: ModelSchema, _=Depends(authorize)):
    for i, model in enumerate(models_db):
        if model.id == model_id:
            updated_model.id = model_id
            models_db[i] = updated_model
            return updated_model
    raise HTTPException(status_code=404, detail="Model not found")


@router.delete("/models/{model_id}", status_code=204)
async def delete_model(model_id: int, _=Depends(authorize)):
    for i, model in enumerate(models_db):
        if model.id == model_id:
            del models_db[i]
            return
    raise HTTPException(status_code=404, detail="Model not found")
