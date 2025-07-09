# CMake generated Testfile for 
# Source directory: D:/data/trae/250708-c-wzq
# Build directory: D:/data/trae/250708-c-wzq/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(test_game_gtest "D:/data/trae/250708-c-wzq/build/test_game_gtest.exe")
set_tests_properties(test_game_gtest PROPERTIES  _BACKTRACE_TRIPLES "D:/data/trae/250708-c-wzq/CMakeLists.txt;34;add_test;D:/data/trae/250708-c-wzq/CMakeLists.txt;0;")
add_test(test_ai_gtest "D:/data/trae/250708-c-wzq/build/test_ai_gtest.exe")
set_tests_properties(test_ai_gtest PROPERTIES  _BACKTRACE_TRIPLES "D:/data/trae/250708-c-wzq/CMakeLists.txt;38;add_test;D:/data/trae/250708-c-wzq/CMakeLists.txt;0;")
add_test(test_gui_gtest "D:/data/trae/250708-c-wzq/build/test_gui_gtest.exe")
set_tests_properties(test_gui_gtest PROPERTIES  _BACKTRACE_TRIPLES "D:/data/trae/250708-c-wzq/CMakeLists.txt;42;add_test;D:/data/trae/250708-c-wzq/CMakeLists.txt;0;")
subdirs("third_party/googletest-1.14.0")
