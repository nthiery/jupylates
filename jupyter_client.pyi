from typing import Any, Dict

class KernelManager:
    def __init__(self, kernel_name: str) -> None:
        pass
    
    def start_kernel(self) -> None:
        pass

    def shutdown_kernel(self) -> None:
        pass

    def request_shutdown(self) -> None:
        pass

    def finish_shutdown(self) -> None:
        pass

    def client(self) -> KernelClient:
        pass

    def is_alive(self) -> bool:
        pass

class KernelClient:
    def execute(self, code: str) -> None:
        pass

    def get_iopub_msg(self) -> Dict[str, Any]:
        pass
