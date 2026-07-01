#include <gst/base/gstbasetransform.h>
#include <gst/gst.h>

namespace {

constexpr const char *kMetaName = "simple-cpp-tracker-meta";

GST_DEBUG_CATEGORY_STATIC(gst_simple_cpp_meta_debug);
#define GST_CAT_DEFAULT gst_simple_cpp_meta_debug

struct GstSimpleCppMeta {
  GstBaseTransform parent;
  guint64 frame_number;
};

struct GstSimpleCppMetaClass {
  GstBaseTransformClass parent_class;
};

} // namespace

#define GST_TYPE_SIMPLE_CPP_META (gst_simple_cpp_meta_get_type())
#define GST_SIMPLE_CPP_META(obj)                                                \
  (G_TYPE_CHECK_INSTANCE_CAST((obj), GST_TYPE_SIMPLE_CPP_META,                  \
                              GstSimpleCppMeta))

GType gst_simple_cpp_meta_get_type();

G_DEFINE_TYPE(GstSimpleCppMeta, gst_simple_cpp_meta, GST_TYPE_BASE_TRANSFORM)

namespace {

GstStaticPadTemplate sink_template = GST_STATIC_PAD_TEMPLATE(
    "sink", GST_PAD_SINK, GST_PAD_ALWAYS, GST_STATIC_CAPS_ANY);

GstStaticPadTemplate src_template = GST_STATIC_PAD_TEMPLATE(
    "src", GST_PAD_SRC, GST_PAD_ALWAYS, GST_STATIC_CAPS_ANY);

GstFlowReturn gst_simple_cpp_meta_transform_ip(GstBaseTransform *base,
                                               GstBuffer *buffer) {
  auto *self = GST_SIMPLE_CPP_META(base);
  const guint64 frame_number = self->frame_number++;

  GstCustomMeta *meta = gst_buffer_add_custom_meta(buffer, kMetaName);
  if (meta == nullptr) {
    GST_ERROR_OBJECT(self, "failed to add custom meta '%s'", kMetaName);
    return GST_FLOW_ERROR;
  }

  GstStructure *structure = gst_custom_meta_get_structure(meta);
  gst_structure_set(structure, "frame-number", G_TYPE_UINT64, frame_number, "x",
                    G_TYPE_INT, 100, "y", G_TYPE_INT, 200, nullptr);

  GST_LOG_OBJECT(self, "attached %s: frame-number=%" G_GUINT64_FORMAT
                       ", x=100, y=200",
                 kMetaName, frame_number);

  return GST_FLOW_OK;
}

gboolean plugin_init(GstPlugin *plugin) {
  GST_DEBUG_CATEGORY_INIT(gst_simple_cpp_meta_debug, "simplecppmeta", 0,
                          "simple C++ metadata transform");

  gst_meta_register_custom_simple(kMetaName);

  return gst_element_register(plugin, "simplecppmeta", GST_RANK_NONE,
                              GST_TYPE_SIMPLE_CPP_META);
}

} // namespace

static void gst_simple_cpp_meta_class_init(GstSimpleCppMetaClass *klass) {
  auto *element_class = GST_ELEMENT_CLASS(klass);
  auto *transform_class = GST_BASE_TRANSFORM_CLASS(klass);

  gst_element_class_set_static_metadata(
      element_class, "Simple C++ Metadata", "Transform/Metadata",
      "Attaches simple GstCustomMeta fields to every buffer", "Amir");

  gst_element_class_add_static_pad_template(element_class, &sink_template);
  gst_element_class_add_static_pad_template(element_class, &src_template);

  transform_class->transform_ip = gst_simple_cpp_meta_transform_ip;
}

static void gst_simple_cpp_meta_init(GstSimpleCppMeta *self) {
  self->frame_number = 0;

  gst_base_transform_set_in_place(GST_BASE_TRANSFORM(self), TRUE);
}

GST_PLUGIN_DEFINE(GST_VERSION_MAJOR, GST_VERSION_MINOR, simplecppmeta,
                  "Simple C++ GStreamer metadata plugin", plugin_init, "0.1.0",
                  "MIT", PACKAGE, "https://gstreamer.freedesktop.org/")
