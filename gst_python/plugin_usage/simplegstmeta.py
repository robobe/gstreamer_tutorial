import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

Gst.init(None)

META_NAME = "simple-tracker-meta"


def on_buffer(pad, info):
    buf = info.get_buffer()

    if buf is None:
        return Gst.PadProbeReturn.OK

    meta = buf.get_custom_meta(META_NAME)

    if meta is None:
        return Gst.PadProbeReturn.OK

    st = meta.get_structure()

    print(
        st.get_name(),
        st.get_value("x"),
        st.get_value("y"),
    )

    return Gst.PadProbeReturn.OK


pipeline = Gst.parse_launch(
    "videotestsrc num-buffers=5 ! simplegstmeta ! fakesink name=sink"
)

sink = pipeline.get_by_name("sink")
sink_pad = sink.get_static_pad("sink")
sink_pad.add_probe(Gst.PadProbeType.BUFFER, on_buffer)

bus = pipeline.get_bus()

pipeline.set_state(Gst.State.PLAYING)

while True:
    msg = bus.timed_pop_filtered(
        Gst.SECOND,
        Gst.MessageType.ERROR | Gst.MessageType.EOS,
    )

    if msg is None:
        continue

    if msg.type == Gst.MessageType.ERROR:
        err, debug = msg.parse_error()
        print(f"ERROR: {err}")
        print(f"DEBUG: {debug}")
        break

    if msg.type == Gst.MessageType.EOS:
        break

pipeline.set_state(Gst.State.NULL)
