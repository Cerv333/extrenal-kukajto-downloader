from .base_service_rec import BaseServiceRec
from ...enum import ServiceTypeEnum


class TaskSubProcessServiceRec(BaseServiceRec):
    def __init__(self, str_code: str, single: bool, task_str_code: str, sub_process_str_code: str):
        super().__init__(str_code, single)
        self._task_str_code = task_str_code
        self._sub_process_str_code = sub_process_str_code

    @property
    def service_type(self) -> str:
        return ServiceTypeEnum.TASK_SUB_PROCESS

    @property
    def params(self) -> dict:
        return {
            'task_str_code': self._task_str_code,
            'sub_process_str_code': self._sub_process_str_code
        }

    @classmethod
    def from_dict(cls, str_code: str, single: bool,  data: dict) -> BaseServiceRec:
        return cls(str_code, single, task_str_code=data['task_str_code'], sub_process_str_code=data['sub_process_str_code'])
