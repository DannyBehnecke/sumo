# build a CPack driven installer package

# set(CMAKE_INSTALL_SYSTEM_RUNTIME_LIBS "${INCLUDE_DIRECTORIES}")
# include(InstallRequiredSystemLibraries)

set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Eclipse Simulation of Urban Mobility - A Microscopic Traffic Simulation")
#${MISSING_LINK} is a variable only used when integrating SUMO via "add subdirectory" into other projects. If not used that way, it just is empty
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}${MISSING_LINK}/LICENSE")
set(CPACK_RESOURCE_FILE_README "${CMAKE_CURRENT_SOURCE_DIR}${MISSING_LINK}/README.md")
set(CPACK_PACKAGE_VERSION "${PACKAGE_VERSION}")

message(STATUS "CPACK_GENERATOR: " ${CPACK_GENERATOR})

if("${CPACK_GENERATOR}" STREQUAL "ZIP")
    set(CPACK_PACKAGE_INSTALL_DIRECTORY "sumo-${CPACK_SYSTEM_NAME}-${PACKAGE_VERSION}")
    set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY "1")
    set(CPACK_STRIP_FILES true)
endif()

include(CPack)
