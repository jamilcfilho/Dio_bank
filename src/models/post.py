from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import db


# Criação de tabelas = 'Post'


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    # User fica em minúsculo devido que é o __tablename__ que a classe User recebe. Se ela ainda fosse por exemplo: UserPost, nesse caso seria chamada através de 'user_post' (nada em maiúsculo e ainda coloca-se a separação com o underline)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
