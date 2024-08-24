from pydantic import BaseModel
from edge_service.src.models import MODEL, PROVIDER


class ModelSchema(BaseModel):
    id: int
    name: MODEL
    provider: PROVIDER
    description: str
