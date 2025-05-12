from .service_request import ServiceRequest
from .task_sub_process_service_request import TaskSubProcessServiceRequest
from .web_browser_service_request import WebBrowserServiceRequest
from ...enum import ServiceTypeEnum

service_request_classes = {
    ServiceTypeEnum.TASK_SUB_PROCESS: TaskSubProcessServiceRequest,
    ServiceTypeEnum.WEB_BROWSER: WebBrowserServiceRequest,
}
