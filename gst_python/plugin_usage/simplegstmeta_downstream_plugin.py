import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

Gst.init(None)

pipeline = Gst.parse_launch(
    "videotestsrc num-buffers=5 ! "
    "simplegstmeta ! "
    "usegstmeta ! "
    "fakesink"
)

bus = pipeline.get_bus()

pipeline.set_state(Gst.State.PLAYING)

while True:
    msg = bus.timed_pop_filtered(
        Gst.SECOND,
        (
            Gst.MessageType.ERROR
            | Gst.MessageType.EOS
            | Gst.MessageType.APPLICATION
        ),
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

    if msg.type == Gst.MessageType.APPLICATION:
        st = msg.get_structure()

        if st.get_name() != "used-tracker-meta":
            continue

        print(
            "bus:",
            st.get_value("x"),
            st.get_value("y"),
            st.get_value("total"),
        )

pipeline.set_state(Gst.State.NULL)
