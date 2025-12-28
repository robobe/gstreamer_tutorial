import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

# Create a GStreamer pipeline
pipeline = Gst.parse_launch("videotestsrc ! videoconvert ! autovideosink")

# Start playing the video
pipeline.set_state(Gst.State.PLAYING)

# Creates a main loop to keep the program running.
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pass