from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import settings

from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.naming_conventions)

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return camel_case_to_snake_case(cls.__name__)