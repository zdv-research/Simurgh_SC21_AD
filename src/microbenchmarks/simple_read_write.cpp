#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>
#include <valgrind/callgrind.h>

#define READ_PRIVATE 0
#define WRITE_PRIVATE 1
#ifndef bytes_per_op
#define bytes_per_op 4*1024
#endif

#ifndef op_count
#define op_count 128*1024
#endif

#ifndef mode
#define mode WRITE_PRIVATE
#endif
class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == WRITE_PRIVATE
        set_title("overwrite_private_4k_files");
#elif mode == READ_PRIVATE
        set_title("read_private_4k_files");
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
    //size_t output_length, input_length;
    // unsigned long long op_count, total;
    //struct snappy_env *env;


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
            //cout << "t_compressedbuffer " << thread_id << " :";
            //for (int i = 0; i < bytes_per_op; i++)
            //    cout << t_write[thread_id][i];
            //cout << endl;

        }
    }

    virtual void prepare(const benchmark_settings& settings)
    {
        //cout << "total file count " << op_count << endl;
        //input_length = bytes_per_op;
        //cout << "bytes per op " << bytes_per_op << endl;
        //output_length = snappy_max_compressed_length(input_length);
        //cout << "output lenght" << output_length << endl ;
        for (size_t i = 0; i < bytes_per_op; i++)
        {
            testdata[0][i] = 'a';
            testdata[1][i] = 'b';
            for (size_t d = 0; d < distribute; d++)
            {
                initdata[d][i] = (char)((((i + d) * d) % 255) + 1);
            }
        }

        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                string p1 = prefix + to_string((process_id + 1 << 4) + thread_id + 1) + "_";

                // for (int i = 0; i < settings.operation_per_thread_count; i++) {
                //     p = p1 + to_string(i);

                int fd = open(p1.c_str(), O_CREAT | O_RDWR);
                //write(fd, initdata, bytes_per_op);
                write(fd, initdata[0], bytes_per_op * distribute);
                if (fd > 0)
                    close(fd);
                // }
            }
        }
    };


    virtual void prepare_on_measurement(const benchmark_settings& settings)
    {
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                preloaded_fds.push_back(open((prefix + to_string((process_id + 1 << 4) + thread_id + 1) + "_").c_str(), O_RDWR /*| O_DIRECT | O_FSYNC */));
            }
        }
    }
    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {
        //cout << "inside run managed \n";
        // CALLGRIND_START_INSTRUMENTATION;
        int combined_id = process_id * settings.thread_per_process_count + thread_id;

#if mode == WRITE_PRIVATE
        for (int i = 0; i < current_op_count; i++)
        {
            //snappy_init_env(&env[i]);
            //string up = p1 + to_string(i);
            //string cp = p2 + to_string(i);

            //cout << "read fd number " << ufd << endl;
            ssize_t rerr = pwrite(preloaded_fds[process_id * settings.thread_per_process_count + thread_id], testdata[i % 2], bytes_per_op, (combined_id + ((i * 210999364) >> 16) % distribute) * bytes_per_op);

        }
        close(preloaded_fds[process_id * settings.thread_per_process_count + thread_id]);



#elif mode == READ_PRIVATE

        //string p1 = prefix + to_string((process_id+1 << 4) + thread_id+1) + "_";
        //string p2 = prefix + to_string((process_id+1 << 4) + thread_id+1) + "c_";
        //struct snappy_env env[current_op_count];
        //const char *fname = p1.c_str();
        //int fd = open(fname, O_RDWR);
        for (int i = 0; i < current_op_count; i++)
        {
            //snappy_init_env(&env[i]);
            //string up = p1 + to_string(i);
            //string cp = p2 + to_string(i);

            //cout << "read fd number " << ufd << endl;
            ssize_t rerr = pread(preloaded_fds[process_id * settings.thread_per_process_count + thread_id], t_readbuffer[thread_id], bytes_per_op, (combined_id + ((i * 210999364) >> 16) % distribute) * bytes_per_op);

        }
        close(preloaded_fds[process_id * settings.thread_per_process_count + thread_id]);

#endif
        // CALLGRIND_STOP_INSTRUMENTATION;
    };

    virtual bool test(const benchmark_settings& settings)
    {

#if mode == READ_PRIVATE


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

#elif mode == WRITE_PRIVATE


        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {

                string p2 = prefix + to_string((process_id + 1 << 4) + thread_id + 1) + "c_";
                for (int i = 0; i < settings.operation_per_thread_count; i++)
                {
                    string p = p2 + to_string(i);

                    int fd = open(p.c_str(), 0);
                    if (fd < 0)
                    {
                        cout << "file " << p << " not found" << endl;
                        return false;
                    }
                    close(fd);
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
