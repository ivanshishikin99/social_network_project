from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin


class Comment(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    text: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))