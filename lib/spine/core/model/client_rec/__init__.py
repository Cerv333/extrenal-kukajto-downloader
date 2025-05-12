from typing import Dict, Type

from .base_client_rec import BaseClientRec
from .task_record import TaskRecord
from .task_sub_process_record import TaskSubProcessRecord
from .web_browser_record import WebBrowserRecord
from ...enum import ClientRoleEnum

client_rec_classes: Dict[str, Type[BaseClientRec]] = {
    ClientRoleEnum.TASK: TaskRecord,
    ClientRoleEnum.TASK_SUB_PROCESS: TaskSubProcessRecord,
    ClientRoleEnum.WEB_BROWSER: WebBrowserRecord
}