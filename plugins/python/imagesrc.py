import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstBase", "1.0")

from gi.repository import GObject, Gst, GstBase

Gst.init(None)

WIDTH = 320
HEIGHT = 240
FPS = 30
CHANNELS = 3
FRAME_SIZE = WIDTH * HEIGHT * CHANNELS
DURATION = Gst.SECOND // FPS

CAPS = Gst.Caps.from_string(
    f"video/x-raw,format=RGB,width={WIDTH},height={HEIGHT},framerate={FPS}/1"
)


class SimplePyImageSrc(GstBase.BaseSrc):

    __gstmetadata__ = (
        "SimplePyImageSrc",
        "Source/Video",
        "Generates simple RGB image buffers",
        "Amir",
    )

    __gsttemplates__ = (
        Gst.PadTemplate.new(
            "src",
            Gst.PadDirection.SRC,
            Gst.PadPresence.ALWAYS,
            CAPS,
        ),
    )

    def __init__(self):
        super().__init__()
        self.frame_number = 0
        self.set_format(Gst.Format.TIME)
        self.set_caps(CAPS)

    def do_start(self):
        self.frame_number = 0
        return True

    def do_is_seekable(self):
        return False

    def do_create(self, offset, size, buf):
        data = bytearray(FRAME_SIZE)
        shift = self.frame_number % 256

        for y in range(HEIGHT):
            for x in range(WIDTH):
                index = (y * WIDTH + x) * CHANNELS
                data[index] = (x + shift) % 256
                data[index + 1] = (y + shift) % 256
                data[index + 2] = shift

        buffer = Gst.Buffer.new_allocate(None, FRAME_SIZE, None)
        buffer.fill(0, data)
        buffer.pts = self.frame_number * DURATION
        buffer.dts = buffer.pts
        buffer.duration = DURATION
        buffer.offset = self.frame_number

        self.frame_number += 1

        return Gst.FlowReturn.OK, buffer


GObject.type_register(SimplePyImageSrc)

__gstelementfactory__ = (
    "simplepyimagesrc",
    Gst.Rank.NONE,
    SimplePyImageSrc,
)
