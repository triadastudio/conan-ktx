cmake_minimum_required(VERSION 3.30)
project(test_package)

find_package(ktx REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} ktx::ktx)
