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

if (ENABLE_DEBUG)
    set(CMAKE_BUILD_TYPE Debug)
else ()
    set(CMAKE_BUILD_TYPE RelWithDebInfo)
endif ()

# don't set extra compile flags again if already declared in this scope
# (i.e. this project is included from Bro)
if (NOT EXTRA_COMPILE_FLAGS)
    set(EXTRA_COMPILE_FLAGS "-Wall -Wno-unused")

    if (ENABLE_DEBUG)
        set(EXTRA_COMPILE_FLAGS "${EXTRA_COMPILE_FLAGS} -DDEBUG")
    endif ()

    # Compiler flags may already exist in CMake cache (e.g. when specifying
    # CFLAGS environment variable before running cmake for the the first time)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${EXTRA_COMPILE_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${EXTRA_COMPILE_FLAGS}")
endif ()

########################################################################
## Dependency Configuration

include(FindRequiredPackage)

FindRequiredPackage(Broccoli)
FindRequiredPackage(SWIG)
FindRequiredPackage(PythonLibs)
FindRequiredPackage(PythonInterp)

if (MISSING_PREREQS)
    foreach (prereq ${MISSING_PREREQ_DESCS})
        message(SEND_ERROR ${prereq})
    endforeach ()
    message(FATAL_ERROR "Configuration aborted due to missing prerequisites")
endif ()

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

if (NOT PY_MOD_INSTALL_DIR)
    # the configure wrapper was not used, default to "home" style installation
    set(PY_MOD_INSTALL_DIR ${CMAKE_INSTALL_PREFIX}/lib/python)
endif ()

install(FILES broccoli.py ${CMAKE_CURRENT_BINARY_DIR}/broccoli.pyc
        DESTINATION ${PY_MOD_INSTALL_DIR})
install(TARGETS ${SWIG_MODULE_broccoli_intern_REAL_NAME}
        DESTINATION ${PY_MOD_INSTALL_DIR})

########################################################################
## Build Summary

if (CMAKE_BUILD_TYPE)
    string(TOUPPER ${CMAKE_BUILD_TYPE} BuildType)
endif ()

message(
    "\n================|  PyBroccoli Build Summary  |=================="
    "\n"
    "\nInstall dir:       ${PY_MOD_INSTALL_DIR}"
    "\nDebug mode:        ${ENABLE_DEBUG}"
    "\n"
    "\nCC:                ${CMAKE_C_COMPILER}"
    "\nCFLAGS:            ${CMAKE_C_FLAGS} ${CMAKE_C_FLAGS_${BuildType}}"
    "\nCXX:               ${CMAKE_CXX_COMPILER}"
    "\nCXXFLAGS:          ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_${BuildType}}"
    "\nCPP:               ${CMAKE_CXX_COMPILER}"
    "\n"
    "\n================================================================\n"
)
