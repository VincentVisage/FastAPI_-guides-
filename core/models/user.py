from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile



class User(Base):
    username: Mapped[str] = mapped_column(String(32) ,unique=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")