#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>

#define READ 0
#define WRITE 1

#ifndef bytes_per_op_M
#define bytes_per_op_M 4
#endif

#ifndef mode
#define mode WRITE
#endif

#define used_space_G 100

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == WRITE
        set_title("large_file_write");
#elif mode == READ
        set_title("large_file_read");
#endif
    };

    long file_size_per_worker_B;

    char* buffer;
    int buffer_len;

    vector<int> preloaded_fds;

    virtual void prepare(const benchmark_settings& settings)
    {

        file_size_per_worker_B = (long) used_space_G * 1024 * 1024 * 1024 / (settings.process_count * settings.thread_per_process_count);

        char one_M[1024*1024];
        for (int j = 0; j < 1024*1024; j++) one_M[j] = j * j;

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                string p1 = prefix + to_string(get_combined_id(process_id, thread_id));
                int fd = open(p1.c_str(), O_CREAT | O_RDWR);

#if mode == READ

                for (int i = 0; i < (file_size_per_worker_B / 1024 / 1024); i++) {

                    write(fd, one_M, 1024*1024);
                }

#endif
                
                close(fd);
            }
        }
    };

    virtual void prepare_on_measurement(const benchmark_settings& settings)
    {
        file_size_per_worker_B = (long) used_space_G * 1024 * 1024 * 1024 / (settings.process_count * settings.thread_per_process_count);

        buffer_len = bytes_per_op_M*1024*1024;
        buffer = (char*) malloc(buffer_len);
        for (int j = 0; j < buffer_len; j++) buffer[j] = (char) (j * j);

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                int fd = open((prefix + to_string(get_combined_id(process_id, thread_id))).c_str(), O_RDWR /*| O_DIRECT | O_FSYNC */);
                preloaded_fds.push_back(fd);
            }
        }
    }
    
    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {
        int combined_id = get_combined_id(process_id, thread_id);
        int fd = preloaded_fds[combined_id];

        int efective_op_count = file_size_per_worker_B / (bytes_per_op_M * 1024 * 1024);

        for (int i = 0; i < efective_op_count; i++)
        {
#if mode == WRITE
            write(fd, buffer, buffer_len);
#elif mode == READ
            read(fd, buffer, buffer_len);
#endif
        }

    };

    virtual void postpare_on_measurement(const benchmark_settings& settings)
    {
        free(buffer);
    }

    virtual bool test(const benchmark_settings& settings)
    {
        return true; // TODO
    };

};

void setup(benchmark_base*& benchmark)
{
    benchmark = new concrete_benchmark();
};
