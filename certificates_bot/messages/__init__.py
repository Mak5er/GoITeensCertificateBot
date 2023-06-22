from pathlib import Path

from pydantic import BaseModel


class Messages(BaseModel):
    greeting: str
    enter_name: str
    please_sent_text: str
    certificate_ready: str



def _load_messages(messages_folder: Path) -> Messages:
    ukranian_file = messages_folder.joinpath(Path('./uk.json'))
    return Messages.parse_file(ukranian_file)


messages = _load_messages(Path('./messages'))
