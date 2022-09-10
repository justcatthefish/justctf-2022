#add_executable(flag-printer main.cpp)

add_executable(im_slow main.cpp)
set_target_properties(im_slow PROPERTIES LINK_SEARCH_START_STATIC ON)
set_target_properties(im_slow PROPERTIES LINK_SEARCH_END_STATIC ON)
target_link_libraries(im_slow PRIVATE -static-libgcc -static-libstdc++ -static)
