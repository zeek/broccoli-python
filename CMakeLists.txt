project(PyBroccoli C)
cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
include(cmake/CommonCMakeConfig.cmake)

########################################################################
## Dependency Configuration

include(FindRequiredPackage)

FindRequiredPackage(Broccoli)
FindRequiredPackage(SWIG)
FindRequiredPackage(PythonInterp)

execute_process(COMMAND ${PYTHON_EXECUTABLE}-config --prefix
                OUTPUT_VARIABLE PYTHON_PREFIX
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
                )

if ( PYTHON_PREFIX )
    set(CMAKE_LIBRARY_PATH ${PYTHON_PREFIX}/lib64 ${PYTHON_PREFIX}/lib ${CMAKE_LIBRARY_PATH})
    set(CMAKE_INCLUDE_PATH ${PYTHON_PREFIX}/include ${CMAKE_INCLUDE_PATH})
endif ()

FindRequiredPackage(PythonLibs)

if (MISSING_PREREQS)
    foreach (prereq ${MISSING_PREREQ_DESCS})
        message(SEND_ERROR ${prereq})
    endforeach ()
    message(FATAL_ERROR "Configuration aborted due to missing prerequisites")
endif ()

if (PYTHON_INCLUDE_PATH)
    # CMake 2.6 compatibility -- FindPythonLibs used to set PYTHON_INCLUDE_PATH
    include_directories(BEFORE ${PYTHON_INCLUDE_PATH})
else ()
    include_directories(BEFORE ${PYTHON_INCLUDE_DIR})
endif ()

include_directories(BEFORE ${Broccoli_INCLUDE_DIR})

########################################################################
## Build Python Extension

include(UseSWIG)

swig_add_module(broccoli_intern python broccoli_intern.i)
swig_link_libraries(broccoli_intern ${Broccoli_LIBRARY} ${PYTHON_LIBRARIES})

########################################################################
## Install Files

if (NOT PY_MOD_INSTALL_DIR)
    # the configure wrapper was not used, default to "home" style installation
    set(PY_MOD_INSTALL_DIR lib/python)
endif ()

install(FILES broccoli.py
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
    "\nCPP:               ${CMAKE_C_COMPILER}"
    "\n"
    "\n================================================================\n"
)

include(UserChangedWarning)
