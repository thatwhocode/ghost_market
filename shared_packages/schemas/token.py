from shared_packages.schemas.base import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str