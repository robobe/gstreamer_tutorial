import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstBase", "1.0")

from gi.repository import GObject, Gst, GstBase

Gst.init(None)


class SimpleMeta(GstBase.BaseTransform):

    __gstmetadata__ = (
        "SimpleMeta",
        "Transform",
        "Posts metadata on the bus",
        "Amir"
    )

    __gsttemplates__ = (
        Gst.PadTemplate.new(
            "sink",
            Gst.PadDirection.SINK,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.new_any()
        ),
        Gst.PadTemplate.new(
            "src",
            Gst.PadDirection.SRC,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.new_any()
        ),
    )

    def do_transform_ip(self, buf):

        s = Gst.Structure.new_empty("tracker")

        s.set_value("x", 100)
        s.set_value("y", 200)

        msg = Gst.Message.new_application(
            self,
            s
        )

        self.post_message(msg)

        return Gst.FlowReturn.OK


GObject.type_register(SimpleMeta)

__gstelementfactory__ = (
    "simplemeta",
    Gst.Rank.NONE,
    SimpleMeta
)
