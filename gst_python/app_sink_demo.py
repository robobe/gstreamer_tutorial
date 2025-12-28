import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import numpy as np
import traceback


# Initialize GStreamer
Gst.init(None)

PIPELINE = """
    videotestsrc is-live=true \
    ! video/x-raw,format=RGB,width=640,height=480,framerate=30/1 \
    ! appsink name=sink emit-signals=true sync=false max-buffers=1 drop=true
"""


pipeline = Gst.parse_launch(PIPELINE)
appsink = pipeline.get_by_name("sink")


def sample_to_ndarray(sample: Gst.Sample) -> np.ndarray:
    buf = sample.get_buffer()
    caps = sample.get_caps()
    s = caps.get_structure(0)

    width = s.get_value("width")
    height = s.get_value("height")
    fmt = s.get_value("format")

    ok, info = buf.map(Gst.MapFlags.READ)
    if not ok:
        raise RuntimeError("Failed to map buffer")
    
    try:
        data = info.data
        arr = np.frombuffer(data, dtype=np.uint8)
        expected = height*width*3

        frame = arr.reshape(height
                            , width,3)
        return frame.copy()
    finally:
        buf.unmap(info)

def on_new_sample(sink) -> Gst.FlowReturn:
    sample = sink.emit("pull-sample")
    if sample is None:
        return Gst.FlowReturn.ERROR
    frame = sample_to_ndarray(sample)
    print(frame.shape)
    return Gst.FlowReturn.OK

appsink.connect("new-sample", on_new_sample)
pipeline.set_state(Gst.State.PLAYING)
# Init GObject loop to handle Gstreamer Bus Events
loop = GLib.MainLoop()

try:
    loop.run()
except KeyboardInterrupt:
    pass
except Exception:
    traceback.print_exc()
    loop.quit()

# Stop Pipeline
pipeline.set_state(Gst.State.NULL)