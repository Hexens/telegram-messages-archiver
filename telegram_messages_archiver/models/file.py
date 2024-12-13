from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from telegram_messages_archiver.models import Base

if TYPE_CHECKING:
    from telegram_messages_archiver.models.message import Message


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    message: Mapped["Message"] = relationship(back_populates="file", single_parent=True)
    size: Mapped[int] = mapped_column(BigInteger)
    duration: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ext: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_path: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"File model, id: {self.id}, file_name: {self.name}"
