include(default)

[settings]
os=iOS
os.version=13.0
os.sdk=iphoneos
arch=armv8
compiler=apple-clang
compiler.libcxx=libc++
compiler.cppstd=20

[env]
CXXFLAGS="-fembed-bitcode"
CFLAGS="-fembed-bitcode"
