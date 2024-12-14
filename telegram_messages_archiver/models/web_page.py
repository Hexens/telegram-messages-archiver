from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from telegram_messages_archiver.models import Base

if TYPE_CHECKING:
    from telegram_messages_archiver.models.message import Message


class WebPage(Base):
    __tablename__ = "web_pages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(Text)
    site_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    message: Mapped["Message"] = relationship(
        back_populates="web_page", single_parent=True
    )

    def __repr__(self) -> str:
        return f"WebPage model, id: {self.id}, site_name: {self.site_name}"
