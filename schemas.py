from pydantic import BaseModel


class QueryResponse(BaseModel):
    query: str
    include_resources: bool = False