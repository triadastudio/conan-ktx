include(default)

[settings]
os=Linux
compiler=clang
compiler.version=13
compiler.libcxx=libstdc++11

[env]
CC=/usr/bin/clang-13
CXX=/usr/bin/clang++-13

[conf]
tools.system.package_manager:mode=install
tools.system.package_manager:sudo=True
