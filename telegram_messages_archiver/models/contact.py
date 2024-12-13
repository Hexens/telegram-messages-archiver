from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from telegram_messages_archiver.models import Base

if TYPE_CHECKING:
    from telegram_messages_archiver.models.message import Message


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    message: Mapped["Message"] = relationship(
        back_populates="contact", single_parent=True
    )
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    vcard: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f"Contact model, id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, "
            f"phone: {self.phone}"
        )
