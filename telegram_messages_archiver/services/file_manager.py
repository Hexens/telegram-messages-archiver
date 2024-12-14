import logging
import os


class FileManager:
    UPLOAD_FOLDER = "media"

    @classmethod
    def make_path(cls, dialog_id: int, message_id: int) -> str:

        path = os.path.join(
            cls.UPLOAD_FOLDER,
            str(dialog_id),
            str(message_id),
        )

        if not os.path.exists(path):
            logging.debug(f"PATH DOESN'T EXIST, creating: {path}")
            os.makedirs(path)

        return path
