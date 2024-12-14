import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from telethon.tl.custom import Message as OriginalMessage
from telethon.tl.custom.file import File as FileOriginal
from telethon.tl.types import WebPage as WebPageOriginal, MessageMediaContact

from telegram_messages_archiver.database import Database
from telegram_messages_archiver.models import Message, File, Contact
from telegram_messages_archiver.models.web_page import WebPage
from telegram_messages_archiver.services.file_manager import FileManager


class MessageManager:

    @staticmethod
    def get_last_message(dialog_original_id: int) -> Message | None:
        with Database.get_db() as db:  # type: Session
            stmt = (
                select(Message)
                .where(Message.dialog_original_id == dialog_original_id)
                .order_by(Message.message_original_id.desc())
            )
            return db.scalars(stmt).first()

    @classmethod
    async def save_messages(
        cls,
        original_messages: [OriginalMessage],
        dialog_id: int,
        dialog_original_id: int,
    ):
        for message_original in original_messages:
            await cls.save_message(message_original, dialog_id, dialog_original_id)

    @classmethod
    async def save_message(
        cls, message_original: OriginalMessage, dialog_id: int, dialog_original_id: int
    ):

        logging.debug(f"Got original message: {message_original}")

        message: Message = cls.map_message(
            message_original, dialog_id, dialog_original_id
        )

        with Database.get_db() as db:  # type: Session

            db.add(message)
            db.flush()

            if message_original.file:
                logging.debug(f"File: {message_original.file}")
                file = cls.map_file(message_original.file, message)

                filepath = FileManager.make_path(
                    dialog_id=dialog_id, message_id=message.id
                )

                # The function download_media add file name to path
                # that is why we use additional variable final_path
                final_path = await message_original.download_media(file=filepath)
                logging.debug(f"final_path: {final_path}")

                file.file_path = final_path

                db.add(file)
            if message_original.contact:
                logging.debug(f"Contact: {message_original.contact}")
                contact = cls.map_contact(message_original.contact, message)
                db.add(contact)
            if message_original.web_preview:
                logging.debug(f"web_preview: {message_original.web_preview}")
                web_page = cls.map_web_page(message_original.web_preview, message)
                db.add(web_page)
            db.flush()
            db.commit()

    @classmethod
    def map_message(
        cls, om: OriginalMessage, dialog_id: int, dialog_original_id: int
    ) -> Message:
        return Message(
            dialog_id=dialog_id,
            sender_id=om.sender_id,
            dialog_original_id=dialog_original_id,
            message_original_id=om.id,
            grouped_id=om.grouped_id,
            message=om.text,
            date=om.date,
            edit_date=om.edit_date,
        )

    @classmethod
    def map_file(cls, file: FileOriginal, message: Message) -> File:
        return File(
            message_id=message.id,
            size=file.size,
            duration=file.duration,
            height=file.height,
            width=file.width,
            ext=file.ext,
            mime_type=file.mime_type,
            name=file.name,
        )

    @classmethod
    def map_contact(cls, contact: MessageMediaContact, message: Message) -> Contact:
        return Contact(
            user_id=contact.user_id,
            message_id=message.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            phone=contact.phone_number,
            vcard=contact.vcard,
        )

    @classmethod
    def map_web_page(cls, web_preview: WebPageOriginal, message: Message) -> WebPage:
        return WebPage(
            message_id=message.id,
            url=web_preview.url,
            site_name=web_preview.site_name,
        )

    # @staticmethod
    # def save_messages(messages):
    #     with Database.get_db() as db:  # type: Session
    #         db.execute(insert(Message), messages)
    #         db.commit()
