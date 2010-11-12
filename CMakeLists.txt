########################################################################
## CMake Configuration

cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

# Prohibit in-source builds.
if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not allowed. Please use "
                        "./configure to choose a build directory and "
                        "initialize the build configuration.")
endif ()

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

########################################################################
## Project/Build Configuration

project(PyBroccoli)

if (ENABLE_DEBUG AND ENABLE_RELEASE)
    set(CMAKE_BUILD_TYPE RelWithDebInfo)
elseif (ENABLE_DEBUG AND NOT ENABLE_RELEASE)
    set(CMAKE_BUILD_TYPE Debug)
elseif (NOT ENABLE_DEBUG AND ENABLE_RELEASE)
    set(CMAKE_BUILD_TYPE Release)
endif ()

########################################################################
## Dependency Configuration

find_package(Broccoli REQUIRED)
find_package(SWIG REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(PythonInterp REQUIRED)
include_directories(BEFORE ${Broccoli_INCLUDE_DIR}
                           ${PYTHON_INCLUDE_DIR}
)

########################################################################
## Build Python Extension

include(UseSWIG)

swig_add_module(broccoli_intern python broccoli_intern.i)
swig_link_libraries(broccoli_intern ${Broccoli_LIBRARY} ${PYTHON_LIBRARIES})

########################################################################
## Install Files

# create the byte-compiled module for installation
configure_file(broccoli.py ${CMAKE_CURRENT_BINARY_DIR}/broccoli.py COPYONLY)
set(compileArg "import py_compile; py_compile.compile('broccoli.py')")
install(CODE
    "execute_process(COMMAND ${PYTHON_EXECUTABLE} -c \"${compileArg}\"
                     WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})"
)
install(FILES broccoli.py ${CMAKE_CURRENT_BINARY_DIR}/broccoli.pyc
        DESTINATION ${CMAKE_INSTALL_PREFIX})
install(TARGETS ${SWIG_MODULE_broccoli_intern_REAL_NAME}
        DESTINATION ${CMAKE_INSTALL_PREFIX})

########################################################################
## Build Summary

if (CMAKE_BUILD_TYPE)
    string(TOUPPER ${CMAKE_BUILD_TYPE} BuildType)
endif ()

message(
    "\n================|  PyBroccoli Build Summary  |=================="
    "\n"
    "\nInstall prefix:    ${CMAKE_INSTALL_PREFIX}"
    "\nDebug mode:        ${ENABLE_DEBUG}"
    "\nRelease mode:      ${ENABLE_RELEASE}"
    "\n"
    "\nCC:                ${CMAKE_C_COMPILER}"
    "\nCFLAGS:            ${CMAKE_C_FLAGS} ${CMAKE_C_FLAGS_${BuildType}}"
    "\nCXX:               ${CMAKE_CXX_COMPILER}"
    "\nCXXFLAGS:          ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_${BuildType}}"
    "\nCPP:               ${CMAKE_CXX_COMPILER}"
    "\n"
    "\n================================================================\n"
)
