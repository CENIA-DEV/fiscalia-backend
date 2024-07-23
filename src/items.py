from typing import Any, Dict, List

from pydantic import BaseModel


class UserRequest(BaseModel):
    user: str


class RucRequest(BaseModel):
    rucs_list: List[str]


class RucUpdateRequest(BaseModel):
    ruc: str
    update_dicc: Dict[str, Any]
