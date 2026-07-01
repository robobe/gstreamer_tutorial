import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")

from gi.repository import Gst, GstApp

Gst.init(None)

META_NAME = "simple-tracker-meta"


def print_buffer_meta(buf):
    meta = buf.get_custom_meta(META_NAME)

    if meta is None:
        return

    st = meta.get_structure()

    print(
        st.get_name(),
        st.get_value("x"),
        st.get_value("y"),
    )


pipeline = Gst.parse_launch(
    "videotestsrc num-buffers=5 ! "
    "simplegstmeta ! "
    "appsink name=sink emit-signals=false sync=false"
)

sink = pipeline.get_by_name("sink")
bus = pipeline.get_bus()

pipeline.set_state(Gst.State.PLAYING)

while True:
    msg = bus.timed_pop_filtered(
        0,
        Gst.MessageType.ERROR | Gst.MessageType.EOS,
    )

    if msg is not None:
        if msg.type == Gst.MessageType.ERROR:
            err, debug = msg.parse_error()
            print(f"ERROR: {err}")
            print(f"DEBUG: {debug}")
            break

        if msg.type == Gst.MessageType.EOS:
            break

    sample = sink.try_pull_sample(100 * Gst.MSECOND)

    if sample is None:
        continue

    buf = sample.get_buffer()

    if buf is None:
        continue

    print_buffer_meta(buf)

pipeline.set_state(Gst.State.NULL)
