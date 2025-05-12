from __future__ import annotations

from typing import List, Type

from websocket import create_connection

from config import config
from .session import SpineSession


class SpineClient:
    def __init__(self, url: str):
        self._url = url
        self._sessions: List[SpineSession] = []

    def open_session(self, access_token: str, session_class: Type[SpineSession] = SpineSession) -> SpineSession:
        header = {
            'Authorization': f'Bearer {access_token}',
        }
        ws = create_connection(self._url, header=header)
        session = session_class(ws, on_close=self._remove_session)
        self._sessions.append(session)
        return session

    def _remove_session(self, session: SpineSession):
        if session in self._sessions:
            self._sessions.remove(session)


spine_client = SpineClient(config.SPINE_URL)
