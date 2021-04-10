#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

#define MODE_SHARED_DIR 0
#define MODE_PRIVATE_DIR 1

#ifndef mode
#define mode MODE_SHARED_DIR
#endif

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == MODE_SHARED_DIR
        set_title("create_close_unlink_file_in_shared_dir");
#elif mode == MODE_PRIVATE_DIR
        set_title("create_close_unlink_file_in_private_dir");
#endif
    };

    virtual void prepare(const benchmark_settings& settings)
    {

        // for (size_t process_id = 0; process_id < settings.process_count; process_id++) {
        //     for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++) {
        //         // ...
        //     }
        // }

    };

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {



#if mode == MODE_SHARED_DIR
        int fd;
        string path = prefix + to_string(get_combined_id(process_id, thread_id));
        for (size_t i = 0; i < current_op_count; i++)
        {
            fd = close(open(path.c_str(), O_CREAT | O_RDWR));
            remove(path.c_str());
        }
#elif mode == MODE_PRIVATE_DIR
        int fd;
        string private_dir = prefix + to_string(get_combined_id(process_id, thread_id)) + "/";
        string private_dir_ = private_dir; // Cause of faulty mkdir..
        mkdir(private_dir_.c_str(), 0);
        string path = private_dir + "a";
        for (size_t i = 0; i < current_op_count; i++)
        {
            fd = close(open(path.c_str(), O_CREAT | O_RDWR));
            remove(path.c_str());
        }
#endif
    };

    virtual bool test(const benchmark_settings& settings)
    {
        return true;
    };
};

void setup(benchmark_base*& benchmark)
{
    benchmark = new concrete_benchmark();
};