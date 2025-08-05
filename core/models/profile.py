from datetime import date

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

from .mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from .user import User


class Profile(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    sex: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[date] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    place_of_work: Mapped[str] = mapped_column(nullable=True)
    place_of_education: Mapped[str] = mapped_column(nullable=True)
    is_public: Mapped[bool] = mapped_column(nullable=False)
    user: Mapped["User"] = relationship(back_populates="profile")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)