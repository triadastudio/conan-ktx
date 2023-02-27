from conan import ConanFile
from conan.tools import cmake, build

import os

class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "CMakeDeps", "VirtualRunEnv"
    test_type = "explicit"

    def layout(self):
        cmake.cmake_layout(self)

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cm = cmake.CMake(self)
        cm.configure()
        cm.build()

    def test(self):
        if build.can_run(self):
            bin_path = os.path.join(self.cpp.build.bindirs[0], "test_package")
            ktx_path = os.path.join(self.source_folder, "etc1.ktx")
            self.run("{} {}".format(bin_path, ktx_path), env="conanrun")
