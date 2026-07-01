#include <gst/base/gstbasetransform.h>
#include <gst/gst.h>

struct GstSimple {
  GstBaseTransform parent;
};

struct GstSimpleClass {
  GstBaseTransformClass parent_class;
};

#define GST_TYPE_SIMPLE (gst_simple_get_type())

GType gst_simple_get_type();

G_DEFINE_TYPE(GstSimple, gst_simple, GST_TYPE_BASE_TRANSFORM)

static GstStaticPadTemplate sink_template = GST_STATIC_PAD_TEMPLATE(
    "sink", GST_PAD_SINK, GST_PAD_ALWAYS, GST_STATIC_CAPS_ANY);

static GstStaticPadTemplate src_template = GST_STATIC_PAD_TEMPLATE(
    "src", GST_PAD_SRC, GST_PAD_ALWAYS, GST_STATIC_CAPS_ANY);

static GstFlowReturn gst_simple_transform_ip(GstBaseTransform *base,
                                             GstBuffer *buffer) {
  (void)base;
  (void)buffer;

  return GST_FLOW_OK;
}

static void gst_simple_class_init(GstSimpleClass *klass) {
  GstElementClass *element_class = GST_ELEMENT_CLASS(klass);
  GstBaseTransformClass *transform_class = GST_BASE_TRANSFORM_CLASS(klass);

  gst_element_class_set_static_metadata(
      element_class, "Simple C++ Transform", "Transform",
      "Passes buffers through unchanged", "Amir");

  gst_element_class_add_static_pad_template(element_class, &sink_template);
  gst_element_class_add_static_pad_template(element_class, &src_template);

  transform_class->transform_ip = gst_simple_transform_ip;
}

static void gst_simple_init(GstSimple *self) {
  gst_base_transform_set_in_place(GST_BASE_TRANSFORM(self), TRUE);
}

static gboolean plugin_init(GstPlugin *plugin) {
  return gst_element_register(plugin, "simple", GST_RANK_NONE, GST_TYPE_SIMPLE);
}

GST_PLUGIN_DEFINE(GST_VERSION_MAJOR, GST_VERSION_MINOR, simple,
                  "Simple C++ GStreamer transform plugin", plugin_init, "0.1.0",
                  "MIT", PACKAGE, "https://gstreamer.freedesktop.org/")
