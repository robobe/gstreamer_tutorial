import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

Gst.init(None)

pipeline = Gst.parse_launch(
    "videotestsrc ! simplemeta ! fakesink"
)

bus = pipeline.get_bus()

pipeline.set_state(Gst.State.PLAYING)

while True:

    msg = bus.timed_pop(
        Gst.SECOND
    )

    if not msg:
        continue

    if msg.type == Gst.MessageType.APPLICATION:

        st = msg.get_structure()

        print(
            st.get_name(),
            st.get_value("x"),
            st.get_value("y")
        )

    elif msg.type == Gst.MessageType.EOS:
        break

pipeline.set_state(Gst.State.NULL)