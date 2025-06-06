from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from .base import Base
from .mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    # _user_id_unique = False
    _user_back_populates = 'posts'
    # _user_id_nullable = False



    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )