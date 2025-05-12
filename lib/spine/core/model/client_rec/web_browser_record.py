from .base_client_rec import BaseClientRec
from ...enum import ClientRoleEnum


class WebBrowserRecord(BaseClientRec):
    def __init__(self):
        pass

    @property
    def role(self) -> str:
        return ClientRoleEnum.WEB_BROWSER

    @property
    def params(self) -> dict:
        return None

    @classmethod
    def from_dict(cls, data: dict) -> BaseClientRec:
        return cls()
