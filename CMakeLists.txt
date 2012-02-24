project(PyBroccoli C)
cmake_minimum_required(VERSION 2.6.3 FATAL_ERROR)
include(cmake/CommonCMakeConfig.cmake)

########################################################################
## Dependency Configuration

include(FindRequiredPackage)

FindRequiredPackage(Broccoli)
FindRequiredPackage(SWIG)
FindRequiredPackage(PythonInterp)
FindRequiredPackage(PythonDev)

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/example.i "%module example %{%}")
execute_process(COMMAND ${SWIG_EXECUTABLE} -python
    ${CMAKE_CURRENT_BINARY_DIR}/example.i
    ERROR_VARIABLE SWIG_PYTHON_ERR)
if (SWIG_PYTHON_ERR)
    message(FATAL_ERROR "Swig installation doesn't support Python wrapper generation: ${SWIG_PYTHON_ERR}")
endif ()

if (MISSING_PREREQS)
    foreach (prereq ${MISSING_PREREQ_DESCS})
        message(SEND_ERROR ${prereq})
    endforeach ()
    message(FATAL_ERROR "Configuration aborted due to missing prerequisites")
endif ()

include_directories(BEFORE ${PYTHON_INCLUDE_DIR})
include_directories(BEFORE ${Broccoli_INCLUDE_DIR})

########################################################################
## Build Python Extension

include(UseSWIG)

swig_add_module(broccoli_intern python broccoli_intern.i)
swig_link_libraries(broccoli_intern ${Broccoli_LIBRARY} ${PYTHON_LIBRARIES})
set_source_files_properties(${swig_generated_file_fullname} PROPERTIES
                            COMPILE_FLAGS -fno-strict-aliasing)

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
