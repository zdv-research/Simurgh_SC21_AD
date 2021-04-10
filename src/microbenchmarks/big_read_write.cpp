#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>

#define MODE_READ 0
#define MODE_WRITE 1

#ifndef bytes_per_op
#define bytes_per_op 2*1024*1024
#endif

#ifndef mode
#define mode MODE_READ
#endif

// TODO: make this benchmark MP ready: prepare->prepare_once and add prepare_per_process

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == MODE_WRITE
        set_title("big_write_benchmark");
#elif mode == MODE_READ
        set_title("big_read_benchmark");
#endif
    };

#if bytes_per_op == 4096
    static const size_t distribute = 20000;
#else
    static const size_t distribute = 50;
#endif

    vector<int> preloaded_fds;
    char initdata[distribute][bytes_per_op];
    char testdata[2][bytes_per_op];
    char t_readbuffer[20][bytes_per_op];

    void print(const benchmark_settings& settings)
    {
        cout << "testdata: ";
        for (int i = 0; i < bytes_per_op; i++)
            cout << testdata[i];
        cout << endl;

        for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
        {
            cout << "t_readbuffer " << thread_id << " :";
            for (int i = 0; i < bytes_per_op; i++)
                cout << t_readbuffer[thread_id][i];
            cout << endl;
        }
    }

    virtual void prepare(const benchmark_settings& settings)
    {

        int fd = open((prefix + "test"s).c_str(),  O_CREAT | O_RDWR);

        for (size_t i = 0; i < bytes_per_op; i++)
        {
            testdata[0][i] = 'a';
            testdata[1][i] = 'b';
            for (size_t d = 0; d < distribute; d++)
            {
                initdata[d][i] = (char)((((i + d) * d) % 255) + 1);
            }

        }

        // for (size_t i = 0; i < settings.thread_per_process_count * settings.process_count; i++)
        // {
        //     preloaded_fds.push_back(open((prefix + "test"s).c_str(), 0));
        // }

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                // for (size_t d = 0; d < distribute; d++) {
                //     //pwrite(fd, initdata[d], bytes_per_op, (process_id * settings.thread_per_process_count + thread_id + d) * bytes_per_op);

                // }
                write(fd, initdata[0], bytes_per_op * distribute);

            }
        }

        close(fd);

    };

    virtual void prepare_on_measurement(const benchmark_settings& settings)
    {
        for (size_t i = 0; i < settings.thread_per_process_count * settings.process_count; i++)
        {
            preloaded_fds.push_back(open((prefix + "test"s).c_str(), O_RDWR /*| O_DIRECT */));
        }
    }

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {

        int combined_id = process_id * settings.thread_per_process_count + thread_id;

#if mode == MODE_WRITE

        int fd = preloaded_fds[thread_id];
        for (size_t j = 0; j < current_op_count; j++)
        {
            pwrite(fd, testdata[j % 2], bytes_per_op, (combined_id + j % distribute) * bytes_per_op);
            fsync(fd);
        }

#elif mode == MODE_READ

        int fd = preloaded_fds[thread_id];
        for (size_t j = 0; j < current_op_count; j++)
        {
            pread(fd, t_readbuffer[thread_id], bytes_per_op, (combined_id + ((j * 210999364) >> 16) % distribute) * bytes_per_op);
            fsync(fd);
        }

#endif
    };

    virtual bool test(const benchmark_settings& settings)
    {

#if mode == MODE_WRITE

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                for (size_t j = 0; j < settings.operation_per_thread_count; j++)
                {
                    int fd = preloaded_fds[thread_id];
                    pread(fd, t_readbuffer[thread_id], bytes_per_op, (thread_id * settings.thread_per_process_count + process_id) * bytes_per_op);
                }

            }
        }

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                for (size_t j = 0; j < bytes_per_op; j++)
                {
                    if (t_readbuffer[thread_id][j] != 'a')
                        return false;
                }

            }
        }

#elif mode == MODE_READ

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                for (size_t j = 0; j < bytes_per_op; j++)
                {
                    if (t_readbuffer[thread_id][j] == 0)
                        return false;
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