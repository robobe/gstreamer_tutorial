# GStreamer Python Examples

## Toggle Gazebo And Camera

`toggle_gz_camera.py` switches one display window between `gzimagesrc` and a
local V4L2 camera using `input-selector`.

Run from the repository root:

```sh
python3 gst_python/toggle_gz_camera.py --debug
```

Keyboard controls in the terminal:

```text
g: show Gazebo /camera
c: show local camera
q: quit
```

Use a different camera device:

```sh
python3 gst_python/toggle_gz_camera.py --device /dev/video2
```

The script currently defaults to raw YUYV at `640x480@30`:

```sh
python3 gst_python/toggle_gz_camera.py --camera-format yuyv --width 640 --height 480 --fps 30
```

For MJPG:

```sh
python3 gst_python/toggle_gz_camera.py --camera-format mjpg --width 640 --height 480 --fps 30
```

Use MJPG for modes such as `1280x720` and `1920x1080` if your camera does not
advertise those sizes under YUYV.

For raw YUYV:

```sh
python3 gst_python/toggle_gz_camera.py --camera-format yuyv --width 640 --height 480 --fps 30
```

Test only the camera branch, without Gazebo or `input-selector`:

```sh
python3 gst_python/toggle_gz_camera.py \
  --test-camera --camera-format yuyv --width 640 --height 480 --fps 30 \
  --print-pipeline
```

Use a test source instead of a real camera:

```sh
python3 gst_python/toggle_gz_camera.py \
  --camera-src "videotestsrc is-live=true pattern=ball"
```
