from conan import ConanFile
from conan.tools import cmake, build, files

import os

class KtxConan(ConanFile):
    name = "ktx"
    version = "4.1.0-20230301"
    description = "Khronos Texture library and tool"
    license = "Apache-2.0"
    topics = ("ktx", "texture", "khronos")
    homepage = "https://github.com/KhronosGroup/KTX-Software"
    url = "https://github.com/triadastudio/conan-ktx"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "sse": [True, False],
        "tools": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "sse": True,
        "tools": True,
    }

    @property
    def _has_sse_support(self):
        return self.settings.arch in ["x86", "x86_64"]

    def layout(self):
        cmake.cmake_layout(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if not self._has_sse_support:
            del self.options.sse
        if self.settings.os in ["iOS", "Android", "Emscripten"]:
            # tools are not build by default if iOS, Android or Emscripten
            self.options.tools = False

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        self.requires("lodepng/cci.20200615")
        self.requires("zstd/1.5.0")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            build.check_min_cppstd(self, 11)

    def source(self):
        files.get(self,
                  **self.conan_data["sources"][self.version],
                  strip_root=True)

    def generate(self):
        tc = cmake.CMakeToolchain(self)
        tc.variables["KTX_FEATURE_TOOLS"] = self.options.tools
        tc.variables["KTX_FEATURE_DOC"] = False
        tc.variables["KTX_FEATURE_LOADTEST_APPS"] = False
        tc.variables["KTX_FEATURE_STATIC_LIBRARY"] = not self.options.shared
        tc.variables["KTX_FEATURE_TESTS"] = False
        tc.variables["BASISU_SUPPORT_SSE"] = self.options.get_safe("sse", False)
        tc.generate()

    def build(self):
        cm = cmake.CMake(self)
        cm.configure()
        cm.build()

    def copy_sources_to_package(self, pattern, src, dst):
        files.copy(self,
                   pattern=pattern,
                   src=os.path.join(self.source_folder, src),
                   dst=os.path.join(self.package_folder, dst))

    def package(self):
        cm = cmake.CMake(self)
        cm.configure()
        cm.install()
        files.rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

        self.copy_sources_to_package("astcenc.h", "lib/astc-encoder/Source/", "include")
        self.copy_sources_to_package("LICENSE.md", "", "licenses")
        self.copy_sources_to_package("*", "LICENSES", "licenses")

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "ktx")
        self.cpp_info.set_property("cmake_target_name", "ktx::ktx")
        self.cpp_info.components["libktx"].names["cmake_find_package"] = "ktx"
        self.cpp_info.components["libktx"].names["cmake_find_package_multi"] = "ktx"
        self.cpp_info.components["libktx"].libs = ["ktx"]
        if self.settings.arch == "x86_64":
            self.cpp_info.components["libktx"].libs.append("astcenc-avx2-static")
        self.cpp_info.components["libktx"].defines = [
            "KTX_FEATURE_KTX1", "KTX_FEATURE_KTX2", "KTX_FEATURE_WRITE"
        ]
        if not self.options.shared:
            self.cpp_info.components["libktx"].defines.append("KHRONOS_STATIC")
            stdcpp_library = build.stdcpp_library(self)
            if stdcpp_library:
                self.cpp_info.components["libktx"].system_libs.append(stdcpp_library)
        if self.settings.os == "Windows":
            self.cpp_info.components["libktx"].defines.append("BASISU_NO_ITERATOR_DEBUG_LEVEL")
        elif self.settings.os == "Linux":
            self.cpp_info.components["libktx"].system_libs.extend(["m", "dl", "pthread"])

        if self.options.tools:
            bin_path = os.path.join(self.package_folder, "bin")
            self.output.info("Appending PATH environment variable: {}".format(bin_path))
            self.env_info.PATH.append(bin_path)
