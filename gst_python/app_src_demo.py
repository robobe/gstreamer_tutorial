import sys
import numpy as np
import traceback
import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib


Gst.init(None)

PIPELINE = """
    appsrc name=app_src \
    ! video/x-raw,width=640,height=480,format=BGR,framerate=10/1 \
    ! videoconvert \
    ! autovideosink
    """

def ndarray_to_gst_buffer(array: np.ndarray) -> Gst.Buffer:
    """Converts numpy array to Gst.Buffer"""
    return Gst.Buffer.new_wrapped(array.tobytes())

frame_id = 0
FPS = 10

def on_need_data(appsrc, length):
    global frame_id

    arr = np.random.randint(
        0, 255, (480, 640, 3), dtype=np.uint8
    )

    buf = Gst.Buffer.new_allocate(None, arr.nbytes, None)
    buf.fill(0, arr.tobytes())

    buf.pts = buf.dts = Gst.util_uint64_scale(frame_id, Gst.SECOND, FPS)
    buf.duration = Gst.util_uint64_scale(1, Gst.SECOND, FPS)

    frame_id += 1

    appsrc.emit("push-buffer", buf)
    
def on_message(bus: Gst.Bus, message: Gst.Message, loop: GLib.MainLoop):
    mtype = message.type
    if mtype == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()

    elif mtype == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(err, debug)
        loop.quit()

    elif mtype == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print(err, debug)

    return True

pipeline = Gst.parse_launch(PIPELINE)
app_source = pipeline.get_by_name("app_src")
bus = pipeline.get_bus()
# allow bus to emit messages to main thread
bus.add_signal_watch()
# Start pipeline
pipeline.set_state(Gst.State.PLAYING)
# Init GObject loop to handle Gstreamer Bus Events
loop = GLib.MainLoop()

# Add handler to specific signal
bus.connect("message", on_message, loop)

app_source.connect("need-data", on_need_data)

try:
    loop.run()
except KeyboardInterrupt:
    pass
except Exception:
    traceback.print_exc()
    loop.quit()

# Stop Pipeline
pipeline.set_state(Gst.State.NULL)