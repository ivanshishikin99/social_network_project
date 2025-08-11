from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from .comment import Comment


class Post(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    text: Mapped[str] = mapped_column(nullable=False)
    tags: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comments: Mapped[list["Comment"]] = relationship(cascade="all, delete")