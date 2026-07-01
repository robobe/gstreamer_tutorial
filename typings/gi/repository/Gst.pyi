from typing import Any

MSECOND: int
SECOND: int

class MessageType(int):
    ERROR: MessageType
    EOS: MessageType
    STATE_CHANGED: MessageType
    WARNING: MessageType
    APPLICATION: MessageType

class State(int):
    NULL: State
    READY: State
    PAUSED: State
    PLAYING: State

class FlowReturn(int):
    OK: FlowReturn
    ERROR: FlowReturn

class MapFlags(int):
    READ: MapFlags

class MapInfo:
    data: bytes

class PadProbeReturn(int):
    OK: PadProbeReturn
    DROP: PadProbeReturn
    REMOVE: PadProbeReturn

class PadProbeType(int):
    BUFFER: PadProbeType

class PadDirection(int):
    SINK: PadDirection
    SRC: PadDirection

class PadPresence(int):
    ALWAYS: PadPresence
    SOMETIMES: PadPresence
    REQUEST: PadPresence

class Rank(int):
    NONE: Rank

class Structure:
    @staticmethod
    def new_empty(name: str) -> Structure: ...

    def set_value(self, fieldname: str, value: Any) -> None: ...
    def get_name(self) -> str: ...
    def get_value(self, fieldname: str) -> Any: ...

class Message:
    type: MessageType
    src: Any

    @staticmethod
    def new_application(src: Any, structure: Structure) -> Message: ...

    def get_structure(self) -> Structure: ...
    def parse_error(self) -> tuple[Exception, str | None]: ...
    def parse_state_changed(self) -> tuple[Any, Any, Any]: ...
    def parse_warning(self) -> tuple[Exception, str | None]: ...

class CustomMeta:
    def get_structure(self) -> Structure: ...
    def has_name(self, name: str) -> bool: ...

class Meta:
    @staticmethod
    def register_custom_simple(name: str) -> Any: ...

class Caps:
    @staticmethod
    def new_any() -> Caps: ...

class PadTemplate:
    @staticmethod
    def new(
        name_template: str,
        direction: PadDirection,
        presence: PadPresence,
        caps: Caps,
    ) -> PadTemplate: ...

class PadProbeInfo:
    def get_buffer(self) -> Buffer | None: ...

class Pad:
    def add_probe(self, mask: PadProbeType, callback: Any, *args: Any) -> int: ...

class Bus:
    def timed_pop(self, timeout: int) -> Message | None: ...
    def timed_pop_filtered(
        self,
        timeout: int,
        types: int | MessageType,
    ) -> Message | None: ...
    def add_signal_watch(self) -> None: ...
    def connect(self, detailed_signal: str, handler: Any, *args: Any) -> int: ...

class Element:
    def set_state(self, state: State) -> int: ...
    def get_bus(self) -> Bus: ...
    def get_by_name(self, name: str) -> Any: ...
    def get_static_pad(self, name: str) -> Pad: ...
    def set_property(self, name: str, value: Any) -> None: ...
    def emit(self, signal_name: str, *args: Any) -> Any: ...
    def post_message(self, message: Message) -> bool: ...

class Pipeline(Element):
    pass

class Sample:
    def get_buffer(self) -> Buffer: ...
    def get_caps(self) -> Any: ...

class Buffer:
    pts: int
    dts: int
    duration: int

    @staticmethod
    def new_wrapped(data: bytes) -> Buffer: ...

    @staticmethod
    def new_allocate(allocator: Any, size: int, params: Any) -> Buffer: ...

    def fill(self, offset: int, src: bytes) -> int: ...
    def map(self, flags: int) -> tuple[bool, MapInfo]: ...
    def unmap(self, info: MapInfo) -> None: ...
    def add_custom_meta(self, name: str) -> CustomMeta | None: ...
    def get_custom_meta(self, name: str) -> CustomMeta | None: ...

def init(argv: Any = ...) -> None: ...
def parse_launch(desc: str) -> Pipeline: ...
def util_uint64_scale(val: int, num: int, denom: int) -> int: ...
