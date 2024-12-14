import logging
from time import sleep

from telethon import TelegramClient
from telethon.tl.custom import Message as OriginalMessage

from telegram_messages_archiver.config import Config
from telegram_messages_archiver.models import Dialog
from telegram_messages_archiver.services import DialogManager, MessageManager


class TelegramManager:

    @classmethod
    def connect_to_telegram_and_run(cls):
        api_id = Config.api_id
        api_hash = Config.api_hash
        phone = Config.phone

        logging.debug("Connecting to Telegram server...")
        client = TelegramClient("session_name", api_id, api_hash)

        client.start(phone)
        logging.debug("Connected.")

        with client:
            client.loop.run_until_complete(cls.run(client))

    @classmethod
    async def run(cls, client):
        async for dialog_original in client.iter_dialogs():
            logging.info(
                "Telegram dialog: %s, id: %d", dialog_original.name, dialog_original.id
            )
            dialog = DialogManager.get_dialog_by_original_id(dialog_original.id)
            if dialog is None:
                logging.debug("Save new dialog: %s", dialog_original.name)
                dialog = Dialog(
                    dialog_original_id=dialog_original.id,
                    name=dialog_original.name,
                    archived=dialog_original.archived,
                )
                DialogManager.save_dialog(dialog)

            await cls.manage_messages(
                tg_client=client,
                dialog_entity=dialog_original.entity,
                dialog_id=dialog.id,
                dialog_original_id=dialog_original.id,
            )

    @classmethod
    async def manage_messages(
        cls, tg_client, dialog_entity, dialog_id, dialog_original_id
    ):
        last_message = MessageManager.get_last_message(
            dialog_original_id=dialog_original_id
        )

        last_id = 0
        if last_message:
            logging.debug(last_message)
            last_id = last_message.message_original_id

        logging.debug(f"Getting messages from last id: {last_id}")

        original_messages = await tg_client.get_messages(
            entity=dialog_entity,
            limit=int(Config.message_limit),
            reverse=True,
            min_id=last_id,
        )

        logging.debug(
            f"Count of messages: {len(original_messages)}",
        )

        if not original_messages:
            return

        await MessageManager.save_messages(
            original_messages, dialog_id, dialog_original_id
        )

        # Uncomment this block after app will grou up alpha version
        # sleep(3)
        #
        # await cls.manage_messages(tg_client, dialog_entity, dialog_id, dialog_original_id)
