#include "benchmark_base.hpp"
#include <valgrind/callgrind.h>
#include <unistd.h>
#include <fcntl.h>

#define MODE_4K 0
#define MODE_4M 1

#ifndef mode
#define mode MODE_4M
#endif

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == MODE_4K
        set_title("fallocate_4K");
#elif mode == MODE_4M
        set_title("fallocate_4M");
#endif
    };
    vector<int> preloaded_fds;

    virtual void prepare(const benchmark_settings& settings)
    {

        int fd;
        for (size_t i = 0; i < settings.thread_per_process_count * settings.process_count; i++)
        {
            
            string p = settings.root + to_string(i);
            fd = open(p.c_str(), O_CREAT | O_RDWR);
            close(fd);
        }
    };

    virtual void prepare_on_measurement(const benchmark_settings& settings)
    {
        for (size_t i = 0; i < settings.thread_per_process_count * settings.process_count; i++)
        {
            //cout << "open for fallocate: %d\n" << (settings.root + to_string(i)).c_str();
            preloaded_fds.push_back(open((settings.root + to_string(i)).c_str(), O_RDWR | O_DIRECT ));
        }
    }

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {

        CALLGRIND_START_INSTRUMENTATION;
        int fd = preloaded_fds[get_combined_id(process_id, thread_id)];

        for (size_t j = 0; j < current_op_count; j++)
        {
#if mode == MODE_4K
            fallocate(fd, 0, j * 4096, 4096);
#elif mode == MODE_4M
           fallocate(fd, 0, j * 1024 * 4096, 1024 * 4096);
#endif
            fsync(fd);
        }
        CALLGRIND_STOP_INSTRUMENTATION;
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