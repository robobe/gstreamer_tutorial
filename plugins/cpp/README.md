# Simple C++ GStreamer Plugins

This directory contains two small C++ GStreamer plugins:

- `simple`: the smallest useful `GstBaseTransform` example. Its
  `transform_ip` method only returns `GST_FLOW_OK`.
- `simplecppmeta`: a slightly larger example that attaches `GstCustomMeta`.

## Prerequisites

Install the GStreamer development headers, Meson, Ninja, and a C++ compiler.
On Ubuntu/Debian:

```sh
sudo apt install build-essential meson ninja-build \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  gstreamer1.0-tools gstreamer1.0-plugins-base
```

## Build

From this directory:

```sh
meson setup build
meson compile -C build
```

This creates:

```text
build/gstsimple.so
build/gstsimplecppmeta.so
```

## Run The Simplest Plugin

Point GStreamer at the build directory, then inspect the plugin:

```sh
GST_PLUGIN_PATH="$PWD/build" gst-inspect-1.0 simple
```

Run a basic pipeline:

```sh
GST_PLUGIN_PATH="$PWD/build" gst-launch-1.0 -v \
  videotestsrc num-buffers=5 ! simple ! fakesink
```

Use an absolute plugin path when running from another directory:

```sh
GST_PLUGIN_PATH="/home/user/projects/gstreamer_tutorial/plugins/cpp/build" \
  gst-inspect-1.0 simple
```

## Plugin Structure

The smallest plugin in `gstsimple.cpp` has these pieces:

- Instance struct: `GstSimple`, the per-element object. It embeds
  `GstBaseTransform parent`.
- Class struct: `GstSimpleClass`, the type-level class object. It embeds
  `GstBaseTransformClass parent_class`.
- Type registration: `G_DEFINE_TYPE(...)` connects the structs to GObject.
- Pad templates: declare one always-present sink pad and one always-present
  source pad. This plugin accepts any caps.
- `transform_ip`: called for each buffer. Returning `GST_FLOW_OK` means the
  buffer passed successfully.
- `class_init`: sets metadata, pad templates, and assigns the virtual method.
- `init`: runs per instance. Here it enables in-place transform behavior.
- `plugin_init`: registers the element factory name `simple`.
- `GST_PLUGIN_DEFINE`: exports the shared object as a loadable GStreamer plugin.

## Run The Metadata Plugin

```sh
GST_PLUGIN_PATH="$PWD/build" GST_DEBUG="simplecppmeta:6" gst-launch-1.0 \
  videotestsrc num-buffers=5 ! simplecppmeta ! fakesink
```

```sh
GST_PLUGIN_PATH="$PWD/build" \
  gst-inspect-1.0 simplecppmeta
```
