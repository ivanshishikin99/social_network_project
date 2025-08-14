from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin


class Message(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    text: Mapped[str] = mapped_column(nullable=False)
    sent_from: Mapped[int] = mapped_column(ForeignKey("user.id"))
    sent_to: Mapped[int] = mapped_column(ForeignKey("user.id"))
