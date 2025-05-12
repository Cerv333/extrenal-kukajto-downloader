from .base_client_rec import BaseClientRec
from ...enum import ClientRoleEnum


class TaskSubProcessRecord(BaseClientRec):
    def __init__(self, task_str_code: str, sub_process_str_code: str):
        self._task_str_code = task_str_code
        self._sub_process_str_code = sub_process_str_code

    @property
    def role(self) -> str:
        return ClientRoleEnum.TASK_SUB_PROCESS

    @property
    def params(self) -> dict:
        return {
            'task_str_code': self._task_str_code,
            'sub_process_str_code': self._sub_process_str_code
        }

    @classmethod
    def from_dict(cls, data: dict) -> BaseClientRec:
        return cls(task_str_code=data['task_str_code'], sub_process_str_code=data['sub_process_str_code'])
