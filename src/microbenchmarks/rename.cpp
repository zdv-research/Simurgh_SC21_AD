#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

#define MODE_FILE 0
#define MODE_PARENT_DIR 1
#define MODE_PRIVATE_FILE_TO_SHARED_DIR 2  // This benchmark has a lot string allocs. We don't use it for now..

#ifndef mode
#define mode MODE_FILE
#endif

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == MODE_FILE
        set_title("rename_files");
#elif mode == MODE_PARENT_DIR
        set_title("rename_dirs_with_file");
#elif mode == MODE_PRIVATE_FILE_TO_SHARED_DIR
        set_title("move_private_file_to_shared_dir");
#endif
    };

    vector<string> paths_old;
    vector<string> paths_new;

    virtual void prepare(const benchmark_settings& settings)
    {

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

#if mode == MODE_FILE
                string path = prefix + to_string(get_combined_id(process_id, thread_id)) + "a";
                close(open(path.c_str(), O_CREAT | O_RDWR));
#elif mode == MODE_PARENT_DIR
                string path = prefix + to_string(get_combined_id(process_id, thread_id));
                mkdir(path.c_str(), 0);
                close(open((path + "a/test").c_str(), O_CREAT | O_RDWR));
#elif mode == MODE_PRIVATE_FILE_TO_SHARED_DIR
                string private_dir = prefix + to_string(get_combined_id(process_id, thread_id)) + "/";
                string private_dir_ = private_dir; // cause of faulty mkdir
                mkdir(private_dir_.cstr(), 0);
                for (int i = 0; i < settings.operation_per_thread_count; i++)
                {
                    string private_file = private_dir + to_string(get_combined_id(process_id, thread_id)) + "_" + to_string(i);
                    close(open(private_file.c_str(), O_CREAT | O_RDWR));
                }
#endif

            }
        }

#if mode == MODE_PRIVATE_FILE_TO_SHARED_DIR
        mkdir((prefix + "shared/").c_str(), 0);
#endif



    };

    virtual void prepare_on_measurement(const benchmark_settings& settings)
    {

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

#if mode == MODE_FILE
                paths_old.push_back(prefix + to_string(get_combined_id(process_id, thread_id)) + "a");
                paths_new.push_back(prefix + to_string(get_combined_id(process_id, thread_id)) + "b");
#elif mode == MODE_PARENT_DIR
                paths_old.push_back(prefix + to_string(get_combined_id(process_id, thread_id)) + "a/test");
                paths_new.push_back(prefix + to_string(get_combined_id(process_id, thread_id)) + "b/test");
#endif

            }
        }



    };

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {

        int combined_id = get_combined_id(process_id, thread_id);

#if mode == MODE_PRIVATE_FILE_TO_SHARED_DIR
        string private_dir = prefix + to_string(get_combined_id(process_id, thread_id)) + "/";
        string public_dir = prefix + "shared/";
        for (size_t c = 0; c < current_op_count; c++)
        {
            string private_file = private_dir + to_string(get_combined_id(process_id, thread_id)) + "_" + to_string(c);
            string public_file = public_dir + to_string(get_combined_id(process_id, thread_id)) + "_" + to_string(c);
            rename(private_file.c_str(), public_dir.c_str());
        }
#else

        for (size_t c = 0; c < current_op_count / 2; c++)
        {
            rename(paths_old[combined_id].c_str(), paths_new[combined_id].c_str());
            rename(paths_new[combined_id].c_str(), paths_old[combined_id].c_str());
        }

#endif

    };

    virtual bool test(const benchmark_settings& settings)
    {

        // TODO

        return true;
    };
};

void setup(benchmark_base*& benchmark)
{
    benchmark = new concrete_benchmark();
};