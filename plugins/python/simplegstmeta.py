import ctypes
import ctypes.util

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstBase", "1.0")

from gi.repository import GObject, Gst, GstBase

Gst.init(None)

META_NAME = "simple-tracker-meta"
G_TYPE_INT = 24


class GValue(ctypes.Structure):
    _fields_ = (
        ("g_type", ctypes.c_size_t),
        ("data", ctypes.c_uint64 * 2),
    )


_gst = ctypes.CDLL(ctypes.util.find_library("gstreamer-1.0"))
_gobject = ctypes.CDLL(ctypes.util.find_library("gobject-2.0"))

_gst.gst_custom_meta_get_structure.argtypes = [ctypes.c_void_p]
_gst.gst_custom_meta_get_structure.restype = ctypes.c_void_p
_gst.gst_structure_set_value.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_void_p,
]
_gst.gst_structure_set_value.restype = None

_gobject.g_value_init.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
_gobject.g_value_init.restype = ctypes.c_void_p
_gobject.g_value_set_int.argtypes = [ctypes.c_void_p, ctypes.c_int]
_gobject.g_value_set_int.restype = None
_gobject.g_value_unset.argtypes = [ctypes.c_void_p]
_gobject.g_value_unset.restype = None

Gst.Meta.register_custom_simple(META_NAME)


def set_meta_int(custom_meta, name, value):
    structure = _gst.gst_custom_meta_get_structure(hash(custom_meta))
    gvalue = GValue()

    _gobject.g_value_init(ctypes.byref(gvalue), G_TYPE_INT)
    _gobject.g_value_set_int(ctypes.byref(gvalue), value)
    _gst.gst_structure_set_value(
        structure,
        name.encode("utf-8"),
        ctypes.byref(gvalue),
    )
    _gobject.g_value_unset(ctypes.byref(gvalue))


class SimpleGstMeta(GstBase.BaseTransform):

    __gstmetadata__ = (
        "SimpleGstMeta",
        "Transform",
        "Attaches tracker metadata to buffers with GstMeta",
        "Amir",
    )

    __gsttemplates__ = (
        Gst.PadTemplate.new(
            "sink",
            Gst.PadDirection.SINK,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.new_any(),
        ),
        Gst.PadTemplate.new(
            "src",
            Gst.PadDirection.SRC,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.new_any(),
        ),
    )

    def do_transform_ip(self, buf):
        meta = buf.add_custom_meta(META_NAME)

        if meta is None:
            return Gst.FlowReturn.ERROR

        set_meta_int(meta, "x", 100)
        set_meta_int(meta, "y", 200)

        return Gst.FlowReturn.OK


GObject.type_register(SimpleGstMeta)

__gstelementfactory__ = (
    "simplegstmeta",
    Gst.Rank.NONE,
    SimpleGstMeta,
)
