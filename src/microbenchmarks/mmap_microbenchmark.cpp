#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>

#define READ 0
#define WRITE 1

#ifndef bytes_per_op_K
#define bytes_per_op_K 4
#endif

#ifndef mode
#define mode WRITE
#endif

#define file_size_per_worker_M 1024

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == WRITE
        set_title("mmap_write");
#elif mode == READ
        set_title("mmap_read");
#endif
    };

    vector<int> preloaded_fds;
    vector<void*> preloaded_mmap_begins;

    virtual void prepare(const benchmark_settings& settings)
    {
        char one_K[1024];

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                string p1 = prefix + to_string(get_combined_id(process_id, thread_id));
                int fd = open(p1.c_str(), O_CREAT | O_RDWR);

                for (int i = 0; i < file_size_per_worker_M * 1024; i++) {

                    for (int j = 0; j < 1024; j++) one_K[j] = (char) process_id * thread_id * i * j;

                    write(fd, one_K, 1024);
                }
                
                close(fd);
            }
        }
    };


    virtual void prepare_on_measurement(const benchmark_settings& settings)
    {
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                int fd = open((prefix + to_string(get_combined_id(process_id, thread_id))).c_str(), O_RDWR /*| O_DIRECT | O_FSYNC */);
                preloaded_fds.push_back(fd);

                void* mmap_begin = mmap(NULL, file_size_per_worker_M * 1024 * 1024, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
                preloaded_mmap_begins.push_back(mmap_begin);
            }
        }
    }

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {
        int combined_id = get_combined_id(process_id, thread_id);

        void* mmap_begin = preloaded_mmap_begins[combined_id];

        char buffer[bytes_per_op_K * 1024];

        for (int i = 0; i < current_op_count; i++)
        {
            int ran = i*9999 + i*8888 + i*i*777777;
#if mode == WRITE
            memcpy((char*)mmap_begin + (ran%(file_size_per_worker_M*1024)) - (ran%(bytes_per_op_K*1024)), buffer, bytes_per_op_K * 1024);
#elif mode == READ
            memcpy(buffer, (char*)mmap_begin + (ran%(file_size_per_worker_M*1024)) - (ran%(bytes_per_op_K*1024)), bytes_per_op_K * 1024);
#endif
        }

    };

    virtual bool test(const benchmark_settings& settings)
    {
        return true; // TODO
    };
    
};

void setup(benchmark_base*& benchmark)
{
    benchmark = new concrete_benchmark();
};
