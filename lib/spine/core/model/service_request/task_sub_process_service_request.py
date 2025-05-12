from .service_request import ServiceRequest
from ...enum import ServiceTypeEnum


class TaskSubProcessServiceRequest(ServiceRequest):
    def __init__(self, task_str_code: str, sub_process_str_code: str, blocking: bool):
        super().__init__(blocking)
        self._task_str_code = task_str_code
        self._sub_process_str_code = sub_process_str_code

    @property
    def service_type(self) -> str:
        return ServiceTypeEnum.TASK_SUB_PROCESS

    @property
    def task_str_code(self) -> str:
        return self._task_str_code

    @property
    def sub_process_str_code(self) -> str:
        return self._sub_process_str_code

    @property
    def params(self) -> dict:
        return {
            'task_str_code': self._task_str_code,
            'sub_process_str_code': self._sub_process_str_code
        }

    @classmethod
    def from_dict(cls, blocking: bool, data: dict) -> ServiceRequest:
        return cls(task_str_code=data['task_str_code'], sub_process_str_code=data['sub_process_str_code'], blocking=blocking)
