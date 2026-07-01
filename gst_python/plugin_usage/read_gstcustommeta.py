import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")

from gi.repository import Gst, GstApp

Gst.init(None)

META_NAME = "simple-tracker-meta"

pipeline = Gst.parse_launch(
    "videotestsrc num-buffers=5 ! "
    "simplegstmeta ! "
    "appsink name=sink sync=false"
)

sink = pipeline.get_by_name("sink")

pipeline.set_state(Gst.State.PLAYING)

for _ in range(5):
    sample = sink.pull_sample()
    buf = sample.get_buffer()
    meta = buf.get_custom_meta(META_NAME)

    if meta is None:
        print("no meta")
        continue

    st = meta.get_structure()

    print(
        st.get_name(),
        st.get_value("x"),
        st.get_value("y"),
    )

pipeline.set_state(Gst.State.NULL)
