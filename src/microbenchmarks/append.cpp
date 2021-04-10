#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>

#define MODE_APPEND_TO_ONLY_ONE_FILE 0
#define MODE_APPEND_TO_ONE_FILE_PER_WORKER 1
#define MODE_OPEN_AND_APPEND_TO_DISTINCT_FILES 2

#ifndef bytes_per_op
#define bytes_per_op 4096
#endif

#ifndef initial_size
#define initial_size 2048
#endif

#ifndef mode
#define mode MODE_APPEND_TO_ONLY_ONE_FILE
#endif

// TODO: make this benchmark MP ready: prepare->prepare_once and add prepare_per_process

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == MODE_APPEND_TO_ONLY_ONE_FILE
        set_title("append_to_only_one_file");
#elif mode == MODE_APPEND_TO_ONE_FILE_PER_WORKER
        set_title("append_to_one_file_per_worker");
#elif mode == MODE_OPEN_AND_APPEND_TO_DISTINCT_FILES
        set_title("open_and_append_to_distinct_files");
#endif
    };

    vector<int> preloaded_fds;
    char initial_data[initial_size];
    char append_data[bytes_per_op];

    virtual void prepare(const benchmark_settings& settings)
    {

        for (size_t i = 0; i < initial_size; i++)
        {
            initial_data[initial_size] = 'i';
        }
        for (size_t i = 0; i < bytes_per_op; i++)
        {
            append_data[bytes_per_op] = 'a';
        }

#if mode == MODE_APPEND_TO_ONLY_ONE_FILE
        int fd = open(prefix.c_str(), O_CREAT | O_RDWR);
        write(fd, initial_data, initial_size);
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                preloaded_fds.push_back(fd);
            }
        }
#elif mode == MODE_APPEND_TO_ONE_FILE_PER_WORKER
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                string p = prefix + to_string((process_id + 1 << 4) + thread_id + 1);
                int fd = open(p.c_str(), O_CREAT | O_RDWR);
                write(fd, initial_data, initial_size);
                preloaded_fds.push_back(fd);
            }
        }
#elif mode == MODE_OPEN_AND_APPEND_TO_DISTINCT_FILES
        // Only create, no preloaded fd's
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                string p1 = prefix + to_string((process_id + 1 << 4) + thread_id + 1) + "_";

                for (int i = 0; i < settings.operation_per_thread_count; i++)
                {
                    string p = p1 + to_string(i);

                    int fd = open(p.c_str(), O_CREAT | O_RDWR);
                    write(fd, initial_data, initial_size);
                    if (fd > 0)
                        close(fd);
                }
            }
        }
#endif

    };

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {

#if mode == MODE_APPEND_TO_ONLY_ONE_FILE || mode == MODE_APPEND_TO_ONE_FILE_PER_WORKER

        int fd = preloaded_fds[process_id * settings.thread_per_process_count + thread_id];

        for (size_t j = 0; j < current_op_count; j++)
        {
            write(fd, append_data, bytes_per_op);
            //fsync(fd);
        }

#elif mode == MODE_OPEN_AND_APPEND_TO_DISTINCT_FILES

        string p1 = prefix + to_string((process_id + 1 << 4) + thread_id + 1) + "_";

        for (int i = 0; i < current_op_count; i++)
        {
            string p = p1 + to_string(i);

            int fd = open(p.c_str(), O_RDWR);
            write(fd, append_data, bytes_per_op);
            //fsync(fd);
            close(fd);
        }

#endif

    };

    virtual bool test(const benchmark_settings& settings)
    {
        // TODO;
        return true;
    };


};

void setup(benchmark_base*& benchmark)
{
    benchmark = new concrete_benchmark();
};