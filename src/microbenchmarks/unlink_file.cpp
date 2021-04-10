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
        set_title("unlink_file_in_shared_dir");
#elif mode == MODE_PRIVATE_DIR
        set_title("unlink_file_in_private_dir");
#endif
    };

    virtual void prepare(const benchmark_settings& settings)
    {

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

#if mode == MODE_SHARED_DIR
                int fd;
                string p1 = prefix + to_string(get_combined_id(process_id, thread_id)) + "_";
                for (size_t i = 0; i < settings.operation_per_thread_count; i++)
                {
                    string p = string().append(p1).append(to_string(i));
                    fd = open(p.c_str(), O_CREAT | O_RDWR);
                    if (fd > 0)
                        close(fd);
                }
#elif mode == MODE_PRIVATE_DIR
                int fd;
                string p1 = prefix + to_string(get_combined_id(process_id, thread_id) + 1) + "/";
                string p1_ = p1; // Cause of faulty mkdir..
                mkdir(p1_.c_str(), 0);
                for (size_t i = 0; i < settings.operation_per_thread_count; i++)
                {
                    string p = p1 + to_string(i);
                    fd = open(p.c_str(), O_CREAT | O_RDWR);
                    if (fd > 0)
                        close(fd);
                }
#endif

            }
        }

    };

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {
#if mode == MODE_SHARED_DIR
        int fd;
        string p1 = prefix + to_string(get_combined_id(process_id, thread_id)) + "_";
        for (size_t i = 0; i < current_op_count; i++)
        {
            string p = p1 + to_string(i);
            remove(p.c_str());
            call_dummy_system_call();
        }
#elif mode == MODE_PRIVATE_DIR
        int fd;
        string p1 = prefix + to_string(get_combined_id(process_id, thread_id) + 1) + "/";
        for (size_t i = 0; i < current_op_count; i++)
        {
            string p = p1 + to_string(i);
            remove(p.c_str());
        }
#endif
    };

    virtual bool test(const benchmark_settings& settings)
    {
#if mode == MODE_SHARED_DIR
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                string p1 = prefix + to_string(get_combined_id(process_id, thread_id)) + "_"s;
                for (int i = 0; i < settings.operation_per_thread_count; i++)
                {
                    string p = p1 + to_string(i);

                    int fd = open(p.c_str(), 0);
                    if (fd >= 0)
                    {
                        cout << "file " << p << " found" << endl;
                        return false;
                    }
                }

            }
        }
#endif
        return true;
    };
};

void setup(benchmark_base*& benchmark)
{
    benchmark = new concrete_benchmark();
};