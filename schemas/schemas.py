from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserCenterSchema(UserSchema):
    state: str


class UserSearchSchema(UserCenterSchema):
    center: str
    product: str
    quantity: int = 0


class UserSchemaProduct(UserCenterSchema):
    center: str
