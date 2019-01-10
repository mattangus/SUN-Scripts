cmake_minimum_required(VERSION 3.0)

project(SunScripts)

find_package(OpenCV REQUIRED)
find_package(LibXml2 REQUIRED)

set(CMAKE_CXX_FLAGS "--std=c++11 -fPIC")
set(CMAKE_BUILD_TYPE Debug)

set(MAIN_SRC
	"src/main.cpp"
	#"lib/zupply.cpp"
)
include_directories("include")

include_directories(${OpenCV_INCLUDE_DIRS} ${LIBXML2_INCLUDE_DIR})

add_executable(SunScripts ${MAIN_SRC})
target_link_libraries(SunScripts ${OpenCV_LIBS} ${LIBXML2_LIBRARIES} stdc++fs)
