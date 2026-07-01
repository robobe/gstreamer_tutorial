import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstBase", "1.0")

from gi.repository import GObject, Gst, GstBase

Gst.init(None)

META_NAME = "simple-tracker-meta"


class UseGstMeta(GstBase.BaseTransform):

    __gstmetadata__ = (
        "UseGstMeta",
        "Transform",
        "Reads tracker metadata from buffers",
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
        meta = buf.get_custom_meta(META_NAME)

        if meta is None:
            print("usegstmeta: no meta")
            return Gst.FlowReturn.OK

        st = meta.get_structure()
        x = st.get_value("x")
        y = st.get_value("y")
        total = x + y

        print(f"usegstmeta: x={x} y={y} total={total}")

        msg_struct = Gst.Structure.new_empty("used-tracker-meta")
        msg_struct.set_value("x", x)
        msg_struct.set_value("y", y)
        msg_struct.set_value("total", total)

        self.post_message(
            Gst.Message.new_application(self, msg_struct)
        )

        return Gst.FlowReturn.OK


GObject.type_register(UseGstMeta)

__gstelementfactory__ = (
    "usegstmeta",
    Gst.Rank.NONE,
    UseGstMeta,
)
