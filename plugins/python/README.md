# Python GStreamer Plugins

This directory contains Python plugins loaded by the GStreamer Python plugin
loader.

## Gazebo Image Source

`gzimagesrc.py` registers an element named `gzimagesrc`. It subscribes to a
Gazebo Harmonic image topic and pushes each received image as a GStreamer raw
video buffer.

The source supports the common 8-bit Gazebo camera formats:

`L_INT8`, `RGB_INT8`, `RGBA_INT8`, `BGRA_INT8`, and `BGR_INT8`.

Run from the repository root:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-inspect-1.0 gzimagesrc
```

Show the camera stream:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-launch-1.0 \
  gzimagesrc topic=/camera ! queue max-size-buffers=1 leaky=downstream ! \
  videoconvert ! autovideosink sync=false
```

If `autovideosink` selects `xvimagesink` and no image appears, choose a sink
explicitly:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-launch-1.0 \
  gzimagesrc topic=/camera ! queue max-size-buffers=1 leaky=downstream ! \
  videoconvert ! ximagesink sync=false
```

You can also verify the source without opening a live window:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-launch-1.0 -q \
  gzimagesrc topic=/camera num-buffers=1 ! videoconvert ! pngenc ! \
  filesink location=/tmp/gz-camera.png
```

Run without opening a window:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-launch-1.0 \
  gzimagesrc topic=/camera num-buffers=30 ! fakesink sync=false
```

The plugin imports Gazebo only when the pipeline starts, so `gst-inspect-1.0`
can still inspect the element even if the Gazebo Python modules are missing.

## Simple Image Source

`imagesrc.py` registers an element named `simplepyimagesrc`. It is a
`GstBase.BaseSrc` element that generates raw RGB video buffers.

The important method is `do_create`. GStreamer calls it whenever downstream
needs another buffer:

```python
def do_create(self, offset, size, buf):
    buffer = Gst.Buffer.new_allocate(None, FRAME_SIZE, None)
    buffer.fill(0, data)
    return Gst.FlowReturn.OK, buffer
```

Run it into a sink:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-launch-1.0 -q \
  simplepyimagesrc num-buffers=60 ! videoconvert ! autovideosink
```

Run it without opening a window:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-launch-1.0 -q \
  simplepyimagesrc num-buffers=5 ! fakesink
```

## Simplest Plugin

`simple.py` registers an element named `simplepy`. It is a
`GstBase.BaseTransform` element with one sink pad, one source pad, and a
minimal in-place transform method:

```python
def do_transform_ip(self, buf):
    return Gst.FlowReturn.OK
```

## Run

Install the GStreamer Python plugin loader first. On Ubuntu/Debian this is
usually:

```sh
sudo apt install python3-gi python3-gst-1.0 gstreamer1.0-python3-plugin-loader
```

Then run from the repository:

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-inspect-1.0 simplepy
```

```sh
GST_PLUGIN_PATH="$PWD/plugins" gst-launch-1.0 -q \
  videotestsrc num-buffers=5 ! simplepy ! fakesink
```

If `gst-inspect-1.0 simplepy` says the element does not exist, the Python
plugin loader is missing, blacklisted, or not in GStreamer's plugin path.

Check for a blacklisted Python loader:

```sh
gst-inspect-1.0 -b
```

If it prints `libgstpython.so`, clear GStreamer's plugin registry cache and
try again:

```sh
rm ~/.cache/gstreamer-1.0/registry.*.bin
GST_PLUGIN_PATH="$PWD/plugins" gst-inspect-1.0 simplepy
```

Why `GST_PLUGIN_PATH="$PWD/plugins"` and not `"$PWD/plugins/python"`:
`libgstpython.so` scans the `python` subdirectory under each plugin path, so
`$PWD/plugins` makes it scan `$PWD/plugins/python`.
