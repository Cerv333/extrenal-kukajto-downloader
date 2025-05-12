from .base_client_rec import BaseClientRec
from ...enum import ClientRoleEnum


class TaskRecord(BaseClientRec):
    def __init__(self, task_str_code: str, execution_id: int):
        self._task_str_code = task_str_code
        self._execution_id = execution_id

    @property
    def role(self) -> str:
        return ClientRoleEnum.TASK

    @property
    def params(self) -> dict:
        return {
            'task_str_code': self._task_str_code,
            'execution_id': self._execution_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> BaseClientRec:
        return cls(task_str_code=data['task_str_code'], execution_id=data['execution_id'])

