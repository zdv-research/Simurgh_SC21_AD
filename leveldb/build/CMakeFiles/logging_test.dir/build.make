# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/salkhordeh/projects/simurghad/leveldb

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/salkhordeh/projects/simurghad/leveldb/build

# Include any dependencies generated for this target.
include CMakeFiles/logging_test.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/logging_test.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/logging_test.dir/flags.make

CMakeFiles/logging_test.dir/util/testharness.cc.o: CMakeFiles/logging_test.dir/flags.make
CMakeFiles/logging_test.dir/util/testharness.cc.o: ../util/testharness.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/salkhordeh/projects/simurghad/leveldb/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/logging_test.dir/util/testharness.cc.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/logging_test.dir/util/testharness.cc.o -c /home/salkhordeh/projects/simurghad/leveldb/util/testharness.cc

CMakeFiles/logging_test.dir/util/testharness.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/logging_test.dir/util/testharness.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/salkhordeh/projects/simurghad/leveldb/util/testharness.cc > CMakeFiles/logging_test.dir/util/testharness.cc.i

CMakeFiles/logging_test.dir/util/testharness.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/logging_test.dir/util/testharness.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/salkhordeh/projects/simurghad/leveldb/util/testharness.cc -o CMakeFiles/logging_test.dir/util/testharness.cc.s

CMakeFiles/logging_test.dir/util/testutil.cc.o: CMakeFiles/logging_test.dir/flags.make
CMakeFiles/logging_test.dir/util/testutil.cc.o: ../util/testutil.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/salkhordeh/projects/simurghad/leveldb/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/logging_test.dir/util/testutil.cc.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/logging_test.dir/util/testutil.cc.o -c /home/salkhordeh/projects/simurghad/leveldb/util/testutil.cc

CMakeFiles/logging_test.dir/util/testutil.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/logging_test.dir/util/testutil.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/salkhordeh/projects/simurghad/leveldb/util/testutil.cc > CMakeFiles/logging_test.dir/util/testutil.cc.i

CMakeFiles/logging_test.dir/util/testutil.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/logging_test.dir/util/testutil.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/salkhordeh/projects/simurghad/leveldb/util/testutil.cc -o CMakeFiles/logging_test.dir/util/testutil.cc.s

CMakeFiles/logging_test.dir/util/logging_test.cc.o: CMakeFiles/logging_test.dir/flags.make
CMakeFiles/logging_test.dir/util/logging_test.cc.o: ../util/logging_test.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/salkhordeh/projects/simurghad/leveldb/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/logging_test.dir/util/logging_test.cc.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/logging_test.dir/util/logging_test.cc.o -c /home/salkhordeh/projects/simurghad/leveldb/util/logging_test.cc

CMakeFiles/logging_test.dir/util/logging_test.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/logging_test.dir/util/logging_test.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/salkhordeh/projects/simurghad/leveldb/util/logging_test.cc > CMakeFiles/logging_test.dir/util/logging_test.cc.i

CMakeFiles/logging_test.dir/util/logging_test.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/logging_test.dir/util/logging_test.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/salkhordeh/projects/simurghad/leveldb/util/logging_test.cc -o CMakeFiles/logging_test.dir/util/logging_test.cc.s

# Object files for target logging_test
logging_test_OBJECTS = \
"CMakeFiles/logging_test.dir/util/testharness.cc.o" \
"CMakeFiles/logging_test.dir/util/testutil.cc.o" \
"CMakeFiles/logging_test.dir/util/logging_test.cc.o"

# External object files for target logging_test
logging_test_EXTERNAL_OBJECTS =

logging_test: CMakeFiles/logging_test.dir/util/testharness.cc.o
logging_test: CMakeFiles/logging_test.dir/util/testutil.cc.o
logging_test: CMakeFiles/logging_test.dir/util/logging_test.cc.o
logging_test: CMakeFiles/logging_test.dir/build.make
logging_test: libleveldb.a
logging_test: CMakeFiles/logging_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/salkhordeh/projects/simurghad/leveldb/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX executable logging_test"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/logging_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/logging_test.dir/build: logging_test

.PHONY : CMakeFiles/logging_test.dir/build

CMakeFiles/logging_test.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/logging_test.dir/cmake_clean.cmake
.PHONY : CMakeFiles/logging_test.dir/clean

CMakeFiles/logging_test.dir/depend:
	cd /home/salkhordeh/projects/simurghad/leveldb/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/salkhordeh/projects/simurghad/leveldb /home/salkhordeh/projects/simurghad/leveldb /home/salkhordeh/projects/simurghad/leveldb/build /home/salkhordeh/projects/simurghad/leveldb/build /home/salkhordeh/projects/simurghad/leveldb/build/CMakeFiles/logging_test.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/logging_test.dir/depend

