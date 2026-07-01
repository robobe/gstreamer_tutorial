import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

Gst.init(None)

PIPELINE = "videotestsrc ! videoconvert ! autovideosink"

pipeline = Gst.parse_launch(PIPELINE)

bus = pipeline.get_bus()

pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        msg = bus.timed_pop_filtered(
            100 * Gst.MSECOND,  # timeout
            Gst.MessageType.ERROR
            | Gst.MessageType.EOS
            | Gst.MessageType.STATE_CHANGED
        )

        if msg is None:
            continue

        if msg.type == Gst.MessageType.ERROR:
            err, debug = msg.parse_error()
            print(f"ERROR: {err}")
            print(f"DEBUG: {debug}")
            break

        elif msg.type == Gst.MessageType.EOS:
            print("End of stream")
            break

        elif msg.type == Gst.MessageType.STATE_CHANGED:
            if msg.src == pipeline:
                old, new, pending = msg.parse_state_changed()
                print(
                    f"Pipeline state changed: "
                    f"{old.value_nick} -> {new.value_nick}"
                )

except KeyboardInterrupt:
    print("Interrupted")

finally:
    pipeline.set_state(Gst.State.NULL)