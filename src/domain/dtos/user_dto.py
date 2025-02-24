from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str
    login: str
    password: str
    created_at: str
    updated_at: str
    deleted_at: str

    class Config:
        from_attributes = True


class UserCreateDTO(BaseModel):
    login: str
    password: str

    class Config:
        from_attributes = True
