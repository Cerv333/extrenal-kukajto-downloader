from .base_service_rec import BaseServiceRec
from .task_sub_process_service_rec import TaskSubProcessServiceRec
from .web_browser_service_rec import WebBrowserServiceRec
from ...enum import ServiceTypeEnum

service_rec_classes = {
    ServiceTypeEnum.TASK_SUB_PROCESS: TaskSubProcessServiceRec,
    ServiceTypeEnum.WEB_BROWSER: WebBrowserServiceRec,
}