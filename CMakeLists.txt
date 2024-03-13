cmake_minimum_required(VERSION 3.5.0)
project(pxd_shader VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

################################################################################
## GLOBAL DEFINITIONS

set(CMAKE_BUILD_TYPE Debug)

list(APPEND CMAKE_CXX_COMPILER_LAUNCHER "ccache")

set(HEADER_FILES
    sources/common.h
    third-party/SIMDString/SIMDString.h
)

set(SOURCE_FILES
    main.cpp

    sources/common.cpp

    third-party/SIMDString/SIMDString.cpp
    ${HEADER_FILES}
)

include_directories(
    sources
    third-party/SIMDString
)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(
    ${PROJECT_NAME} PRIVATE)

target_precompile_headers(
    ${PROJECT_NAME} PRIVATE
    ${HEADER_FILES}
    <format>
    <filesystem>
)

target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_20)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
