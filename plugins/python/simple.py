import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstBase", "1.0")

from gi.repository import GObject, Gst, GstBase

Gst.init(None)


class SimplePy(GstBase.BaseTransform):

    __gstmetadata__ = (
        "SimplePy",
        "Transform",
        "Passes buffers through unchanged",
        "Amir",
    )

    __gsttemplates__ = (
        Gst.PadTemplate.new(
            "sink",
            Gst.PadDirection.SINK,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.new_any(),
        ),
        Gst.PadTemplate.new(
            "src",
            Gst.PadDirection.SRC,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.new_any(),
        ),
    )

    def do_transform_ip(self, buf):
        return Gst.FlowReturn.OK


GObject.type_register(SimplePy)

__gstelementfactory__ = (
    "simplepy",
    Gst.Rank.NONE,
    SimplePy,
)
