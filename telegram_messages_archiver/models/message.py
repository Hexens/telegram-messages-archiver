from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from telegram_messages_archiver.models.base import Base

if TYPE_CHECKING:
    from telegram_messages_archiver.models.file import File
    from telegram_messages_archiver.models.contact import Contact
    from telegram_messages_archiver.models.web_page import WebPage


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    dialog_id: Mapped[int] = mapped_column(BigInteger)
    sender_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    dialog_original_id: Mapped[int] = mapped_column(BigInteger)
    message_original_id: Mapped[int] = mapped_column(BigInteger)
    grouped_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    date: Mapped[datetime]
    edit_date: Mapped[Optional[datetime]]
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file: Mapped[Optional["File"]] = relationship(back_populates="message")
    contact: Mapped[Optional["Contact"]] = relationship(back_populates="message")
    web_page: Mapped[Optional["WebPage"]] = relationship(back_populates="message")

    def __repr__(self) -> str:
        return f"Message model, id: {self.id}, date: {self.date}, message_original_id: {self.message_original_id}"
