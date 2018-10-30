from   conans       import ConanFile, CMake, tools
from   conans.tools import download, unzip, os_info
from   distutils.dir_util import copy_tree
import os
import shutil
import multiprocessing

# http://gainput.johanneskuhlmann.de/api/page_building.html
class GainputConan(ConanFile):
    name            = "gainput"
    version         = "master"
    description     = "Conan package for gainput."
    url             = "https://github.com/jkuhlmann/gainput"
    license         = "MIT"
    settings        = "arch", "build_type", "compiler", "os"
    generators      = "cmake"
    exports_sources = "lib/source/*"
    options         = {
      "shared": [True, False],
      "gainput_debug": [True, False],
      "gainput_dev": [True, False],
      "gainput_enable_recorder": [True, False],
      "gainput_lib_build": [True, False]
    }
    default_options = \
      "shared=False", \
      "gainput_debug=False", \
      "gainput_dev=False", \
      "gainput_enable_recorder=False", \
      "gainput_lib_build=True",

    def source(self):
        self.run("git clone git://github.com/jkuhlmann/gainput.git")

    def build(self):
        cmake = CMake(self)
        #if self.options.shared:
        #  cmake.definitions["GAINPUT_BUILD_STATIC"] = "OFF"
        #else:
        #  cmake.definitions["GAINPUT_BUILD_SHARED"] = "OFF"
        if self.options.gainput_debug:
          cmake.definitions["GAINPUT_DEBUG"] = "ON"
        if self.options.gainput_dev:
          cmake.definitions["GAINPUT_DEV"] = "ON"
        if self.options.gainput_enable_recorder:
          cmake.definitions["GAINPUT_ENABLE_RECORDER"] = "ON"
        if self.options.gainput_lib_build:
          cmake.definitions["GAINPUT_LIB_BUILD"] = "ON"
        cmake.configure(source_folder="gainput")
        cmake.build()

    def collect_headers(self, include_folder):
        self.copy("*.h"  , dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)

    def package(self):
        self.collect_headers("gainput/lib/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["gainput"]
