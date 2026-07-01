import argparse
import os
import sys

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import GLib, Gst


def bool_string(value):
    return "true" if value else "false"


def build_pipeline_description(args):
    caps = (
        "video/x-raw,"
        f"format=RGBA,width={args.width},height={args.height},framerate={args.fps}/1"
    )
    camera_src = args.camera_src or build_v4l2_source(args)

    return f"""
        input-selector name=selector sync-streams=false cache-buffers=false !
            queue !
            videoconvert !
            glimagesink sync=false

        gzimagesrc name=gz_src topic={args.topic} debug={bool_string(args.debug)} !
            queue name=gz_queue max-size-buffers=1 leaky=downstream !
            videoconvert !
            videoscale !
            videorate !
            {caps} !
            queue !
            selector.sink_0

        {camera_src} !
            queue name=camera_queue max-size-buffers=1 leaky=downstream !
            videoconvert !
            videoscale !
            videorate !
            {caps} !
            queue !
            selector.sink_1
    """


def build_pipeline(args):
    pipeline_description = build_pipeline_description(args)
    if args.print_pipeline:
        print(pipeline_description, flush=True)

    return Gst.parse_launch(pipeline_description)


def build_camera_test_pipeline_description(args):
    caps = (
        "video/x-raw,"
        f"format=RGBA,width={args.width},height={args.height},framerate={args.fps}/1"
    )
    camera_src = args.camera_src or build_v4l2_source(args)
    return f"""
        {camera_src} !
            queue max-size-buffers=1 leaky=downstream !
            videoconvert !
            videoscale !
            videorate !
            {caps} !
            fakesink sync=false
    """


def build_v4l2_source(args):
    if args.camera_format == "mjpg":
        return (
            f"v4l2src device={args.device} do-timestamp=true ! "
            f"image/jpeg,width={args.width},height={args.height},"
            f"framerate={args.fps}/1 ! "
            "jpegparse ! "
            "jpegdec"
        )

    return (
        f"v4l2src device={args.device} do-timestamp=true ! "
        f"video/x-raw,format=YUY2,width={args.width},height={args.height},"
        f"framerate={args.fps}/1"
    )


def set_active_source(selector, source_name):
    pad_name = "sink_0" if source_name == "gazebo" else "sink_1"
    pad = selector.get_static_pad(pad_name)
    if pad is None:
        print(f"missing selector pad {pad_name}", flush=True)
        return

    selector.set_property("active-pad", pad)
    print(f"active source: {source_name}", flush=True)


def on_keyboard(source, condition, selector, loop):
    if condition & GLib.IOCondition.HUP:
        loop.quit()
        return False

    line = sys.stdin.readline()
    if line == "":
        loop.quit()
        return False

    command = line.strip().lower()

    if command == "g":
        set_active_source(selector, "gazebo")
    elif command == "c":
        set_active_source(selector, "camera")
    elif command == "q":
        loop.quit()
        return False
    else:
        print("press g for Gazebo, c for camera, q to quit", flush=True)

    return True


def on_message(bus, message, loop):
    message_type = message.type

    if message_type == Gst.MessageType.ERROR:
        error, debug = message.parse_error()
        print(f"error: {error}", flush=True)
        if debug:
            print(f"debug: {debug}", flush=True)
        loop.quit()
    elif message_type == Gst.MessageType.WARNING:
        warning, debug = message.parse_warning()
        print(f"warning: {warning}", flush=True)
        if debug:
            print(f"debug: {debug}", flush=True)
    elif message_type == Gst.MessageType.EOS:
        print("end of stream", flush=True)
        loop.quit()

    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Toggle display between gzimagesrc and a local camera."
    )
    parser.add_argument("--topic", default="/camera", help="Gazebo image topic")
    parser.add_argument("--device", default="/dev/video0", help="v4l2 camera device")
    parser.add_argument(
        "--camera-src",
        help=(
            "Custom camera source description. Example: "
            "'videotestsrc is-live=true pattern=ball'"
        ),
    )
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument(
        "--camera-format",
        choices=("mjpg", "yuyv"),
        default="yuyv",
        help="Camera capture format to request from v4l2src",
    )
    parser.add_argument("--start", choices=("gazebo", "camera"), default="camera")
    parser.add_argument(
        "--print-pipeline",
        action="store_true",
        help="Print the generated GStreamer pipeline before starting",
    )
    parser.add_argument(
        "--test-camera",
        action="store_true",
        help="Run only the camera branch into fakesink",
    )
    parser.add_argument("--debug", action="store_true", help="Enable gzimagesrc debug")
    return parser.parse_args()


def main():
    args = parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugin_path = os.path.join(repo_root, "plugins")
    existing_plugin_path = os.environ.get("GST_PLUGIN_PATH")
    os.environ["GST_PLUGIN_PATH"] = (
        plugin_path
        if not existing_plugin_path
        else f"{plugin_path}{os.pathsep}{existing_plugin_path}"
    )

    Gst.init(None)

    if args.test_camera:
        pipeline_description = build_camera_test_pipeline_description(args)
        if args.print_pipeline:
            print(pipeline_description, flush=True)
        pipeline = Gst.parse_launch(pipeline_description)
        selector = None
    else:
        pipeline = build_pipeline(args)
        selector = pipeline.get_by_name("selector")
        if selector is None:
            raise RuntimeError("failed to find input-selector")

    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message, loop)

    if selector is not None:
        set_active_source(selector, args.start)

        print("press g for Gazebo, c for camera, q to quit", flush=True)
        GLib.io_add_watch(
            sys.stdin,
            GLib.IO_IN | GLib.IO_HUP,
            on_keyboard,
            selector,
            loop,
        )

    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    main()
