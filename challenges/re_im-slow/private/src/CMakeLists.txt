cmake_minimum_required(VERSION 3.14)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "-O0 -fno-exceptions -fno-elide-constructors -fdce")
set(CMAKE_CXX_FLAGS_DEBUG "-ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "-DNDEBUG")

project(re-im-slow)

add_subdirectory(src)
add_subdirectory(test)