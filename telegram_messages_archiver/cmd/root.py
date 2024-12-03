import logging

import click
from sqlalchemy import select

from telegram_messages_archiver.config import Config
from telegram_messages_archiver.database import Database
from telegram_messages_archiver.logger import Logger
from telegram_messages_archiver.models import Base, Message


@click.version_option(version="0.1.1", prog_name="Telegram Message Archiver")
@click.option("--api_id", envvar="API_ID", help="Telegram API ID")
@click.option("--api_hash", envvar="API_HASH", help="Telegram API HASH")
@click.option("--phone", envvar="PHONE", help="Telegram phone number")
@click.option("--message_limit", envvar="MESSAGE_LIMIT", help="Telegram message limit")
@click.option("--dsn", envvar="DSN", help="Data Source Name of DataBase")
@click.option("--debug", envvar="DEBUG", help="Show debug messages")
@click.group(invoke_without_command=True)
@click.pass_context
def root(ctx, **kwargs):
    Config.init(**kwargs)
    Database.init()
    Logger.init()
    if ctx.invoked_subcommand:
        return

    logging.info("Command 'telegram-message-archiver' has been started.")

    with Database.get_db() as db:
        message = db.execute(select(Message).order_by(Message.message_id.desc())).first()
        print(message)



@root.command()
def initdb():
    """Initialize the database."""
    logging.info("Initializing database...")
    Base.metadata.drop_all(bind=Database.get_engine())
    Base.metadata.create_all(bind=Database.get_engine())
    logging.info("Database initialized.")
