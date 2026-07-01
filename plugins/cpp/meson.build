project(
  'gstreamer-cpp-examples',
  'cpp',
  version: '0.1.0',
  default_options: [
    'cpp_std=c++17',
    'warning_level=2',
  ],
)

gst_dep = dependency('gstreamer-1.0', version: '>=1.20')
gst_base_dep = dependency('gstreamer-base-1.0', version: '>=1.20')

shared_library(
  'gstsimple',
  'gstsimple.cpp',
  dependencies: [
    gst_dep,
    gst_base_dep,
  ],
  cpp_args: [
    '-DPACKAGE="gstreamer-tutorial"',
  ],
  name_prefix: '',
  install: false,
)

shared_library(
  'gstsimplecppmeta',
  'gstsimplecppmeta.cpp',
  dependencies: [
    gst_dep,
    gst_base_dep,
  ],
  cpp_args: [
    '-DPACKAGE="gstreamer-tutorial"',
  ],
  name_prefix: '',
  install: false,
)
