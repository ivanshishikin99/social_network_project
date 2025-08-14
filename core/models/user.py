from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

from .mixins import IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from .profile import Profile
    from .post import Post
    from .comment import Comment
    from .message import Message


class User(Base, IdIntPkMixin, CreatedAtMixin, UpdatedAtMixin):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(nullable=False)
    role_access: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    profile: Mapped["Profile"] = relationship(back_populates="user", cascade="all, delete")
    posts: Mapped[list["Post"]] = relationship(cascade="all, delete")
    comments: Mapped[list["Comment"]] = relationship(cascade="all, delete")
    messages: Mapped[list["Message"]] = relationship(cascade="all, delete")
