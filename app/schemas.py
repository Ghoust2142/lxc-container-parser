from pydantic import BaseModel
from typing import List, Optional


class ContainerIPDTO(BaseModel):
    ip_address: str
    family: Optional[str] = None


class ContainerDTO(BaseModel):
    name: str
    cpu_usage: int
    memory_usage: int
    created_at_utc: int
    status: str
    ips: List[ContainerIPDTO]

