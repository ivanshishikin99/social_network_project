from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

from .mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from .profile import Profile


class User(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    verified: Mapped[str] = mapped_column(nullable=False)
    role_access: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    profile: Mapped["Profile"] = relationship(back_populates="user")
