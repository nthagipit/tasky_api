from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    id: str
    email: str

    model_config = ConfigDict(from_attributes=True)

