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

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["GAINPUT_DEBUG"] = self.options.gainput_debug
        cmake.definitions["GAINPUT_DEV"] = self.options.gainput_dev
        cmake.definitions["GAINPUT_ENABLE_RECORDER"] = self.options.gainput_enable_recorder
        cmake.definitions["GAINPUT_LIB_BUILD"] = self.options.gainput_lib_build
        cmake.configure()
        return cmake

    def source(self):
        self.run("git clone git://github.com/jkuhlmann/gainput.git")
        copy_tree("gainput", ".")

    def build(self):
        cmake = CMake(self)
        cmake = self.configure_cmake()
        cmake.build()

    def collect_headers(self, include_folder):
        self.copy("*.h"  , dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)

    def package(self):
        self.collect_headers("lib/include")
        self.copy("*.a"  , dst="lib", keep_path=False)
        self.copy("*.so" , dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
