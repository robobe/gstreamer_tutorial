#!/usr/bin/env python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)

# Define pipeline string using input-selector
pipeline_str = """
input-selector name=selector !
    videoconvert ! autovideosink
    v4l2src device=/dev/video0 ! videoconvert ! selector.sink_0
    v4l2src device=/dev/video4 ! videoconvert ! selector.sink_1
"""

print("Pipeline:\n", pipeline_str)
pipeline = Gst.parse_launch(pipeline_str)

selector = pipeline.get_by_name("selector")
pads = selector.sinkpads

# state for switching
current_index = {"i": 0}

def switch_source():
    current_index["i"] = (current_index["i"] + 1) % len(pads)
    pad = pads[current_index["i"]]
    selector.set_property("active-pad", pad)
    print(f"Switched to camera {current_index['i']}")
    return True  # keep repeating

# Set up bus to catch errors and EOS
bus = pipeline.get_bus()
bus.add_signal_watch()

def on_message(bus, message):
    if message.type == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error:", err, debug)
        loop.quit()
    elif message.type == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()

bus.connect("message", on_message)

# Start pipeline
pipeline.set_state(Gst.State.PLAYING)

# Switch every 5 seconds
GLib.timeout_add_seconds(5, switch_source)

loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pass
finally:
    pipeline.set_state(Gst.State.NULL)