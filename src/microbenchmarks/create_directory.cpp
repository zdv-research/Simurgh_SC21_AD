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
        set_title("create_dir_in_shared_dir");
#elif mode == MODE_PRIVATE_DIR
        set_title("create_dir_in_private_dir");
#endif
    };

    virtual void prepare(const benchmark_settings& settings)
    {

    };

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {

#if mode == MODE_SHARED_DIR
        string path_prefix = prefix + to_string(get_combined_id(process_id, thread_id)) + "_";
        for (size_t i = 0; i < current_op_count; i++)
        {
            string p = path_prefix + to_string(i);
            mkdir(p.c_str(), 0);
        }
#elif mode == MODE_PRIVATE_DIR
        string dir = prefix + to_string(get_combined_id(process_id, thread_id)) + "/";
        string dir_ = dir; // Cause of faulty mkdir..
        mkdir(dir_.c_str(), 0);
        for (size_t i = 0; i < current_op_count; i++)
        {
            string p = dir + to_string(i);
            mkdir(p.c_str(), 0);
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