cmake_minimum_required(VERSION 2.8.12)
project(test_package)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test_package gainput_test.cpp)
target_link_libraries(test_package ${CONAN_LIBS})

set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)