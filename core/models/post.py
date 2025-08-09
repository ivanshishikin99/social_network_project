from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin


class Post(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    text: Mapped[str] = mapped_column(nullable=False)
    tags: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))