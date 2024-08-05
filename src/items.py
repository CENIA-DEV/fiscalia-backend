from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class UserRequest(BaseModel):
    user: str


class RucRequest(BaseModel):
    rucs_list: List[str]


class RucUpdateRequest(BaseModel):
    ruc: str
    update_dicc: Dict[str, Any]


class RucSearchRequest(BaseModel):
    grupo_delito: Optional[str] = None
    estado: Optional[str] = None
    fecha: Optional[str] = None
