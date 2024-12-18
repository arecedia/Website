from sqlalchemy.util import deprecated
from sqlmodel import SQLModel, Field
import uuid
from passlib.context import CryptContext
from dataclasses import field

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str
    password: str
    admin: bool

    def verify_password(self, password):
        if password is None:
            return False
        return pwd_context.verify(password, self.password)

    def update_password(self, password):
        if password is None:
            return False
        elif password != "":
            new_password = hash_password(password)
            self.password = new_password

class PublicUser(SQLModel):
    id: uuid.UUID
    username: str

class CreateUser(SQLModel):
    username: str
    email: str
    password: str

class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    admin: bool | None = None
