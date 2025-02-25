from pydantic import BaseModel, field_validator


class Token(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class Login(BaseModel):
    login: str
    password: str

    class Config:
        from_attributes = True


class Register(BaseModel):
    login: str
    password: str

    class Config:
        from_attributes = True

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value

    @field_validator('login')
    def validate_login(cls, value: str) -> str:
        if len(value) < 4:
            raise ValueError('Login must be at least 4 characters long')
        return value
