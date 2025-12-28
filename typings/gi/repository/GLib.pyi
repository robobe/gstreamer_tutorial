from typing import Any
from typing import Annotated

@staticmethod
def MainLoop() -> Annotated["MainLoop", "Create a new GLib main loop"]: ...
    

class MainLoop:
    def run(self) -> None: ...
    def quit(self) -> None: ...