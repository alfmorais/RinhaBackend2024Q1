from enum import Enum

from pydantic import BaseModel, Field


class TypeEnum(Enum):
    credit = "c"
    debit = "d"


class Transactions(BaseModel):
    amount: int = Field(alias="valor", gt=0)
    type: TypeEnum = Field(alias="tipo")
    description: str = Field(alias="descricao", max_length=10, min_length=1)
