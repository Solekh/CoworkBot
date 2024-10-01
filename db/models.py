import asyncio
import datetime
from dataclasses import dataclass
from datetime import date

from pydantic.v1 import BaseModel
from pydantic.v1 import validator

from bot.enums import RoleEnum, LangEnum
from db.config import CRUD


class UserJob(CRUD, BaseModel):
    id: int = None
    user_id: int = None
    job_id: int = None


class User(CRUD, BaseModel):
    id: int = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    language: str = LangEnum.en.name
    description: str = None
    balance: float = 0
    role: list[str] = [RoleEnum.user.name]

    @classmethod
    @validator('phone_number')
    def phone_number_validator(cls, phone_number):
        return phone_number.removeprefix("+")

    @classmethod
    @validator('role')
    def role_validator(cls, role):
        if role in RoleEnum.value:
            return RoleEnum(role).name

    @property
    async def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Category(CRUD, BaseModel):
    id: int = None
    name: str = None


class Job(CRUD, BaseModel):
    id: int = None
    name: str = None
    category_id: int = None

    async def filter_by_category(self):
        jobs: list[Job] = await self.objects
        result = []
        for job in jobs:
            if job.category_id == self.category_id:
                result.append(job)
        return result


class Project(CRUD, BaseModel):
    id: int = None
    name: str = None
    description: str = None
    price: float = None
    status: bool = True
    document: str = None
    category_id: int = None
    owner_id: int = None
    created_at: str = str(datetime.datetime.now())


class Order(CRUD, BaseModel):
    id: int = None
    project_id: int = None
    employee_id: int = None
    is_payment: int = False
