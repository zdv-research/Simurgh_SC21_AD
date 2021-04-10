#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

#define MODE_SHARED_DIR 0
#define MODE_PRIVATE_DIR 1
#define MODE_SINGLE_FILE 2

#ifndef mode
#define mode MODE_SHARED_DIR
#endif

class concrete_benchmark : public benchmark_base
{
public:
    concrete_benchmark()
    {
#if mode == MODE_SHARED_DIR
        set_title("path_resolution_depth_5_shared_dir");
#elif mode == MODE_PRIVATE_DIR
        set_title("path_resolution_depth_5_private_dir");
#elif mode == MODE_SINGLE_FILE
        set_title("path_resolution_depth_5_single_file");
#endif
    };

    virtual void prepare(const benchmark_settings& settings)
    {

        mkdir(prefix.c_str(), 0);

#if mode == MODE_SHARED_DIR

        mkdir((prefix + "1").c_str(), 0);
        mkdir((prefix + "1/2").c_str(), 0);
        mkdir((prefix + "1/2/3").c_str(), 0);
        mkdir((prefix + "1/2/3/4").c_str(), 0);
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                int fd = open((prefix + "1/2/3/4/" + to_string(get_combined_id(process_id, thread_id))).c_str(), O_CREAT | O_RDWR);
                if (fd > 0)
                    close(fd);
            }
        }
#elif mode == MODE_PRIVATE_DIR
        for (size_t process_id = 0; process_id < settings.process_count; process_id++)
        {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++)
            {
                string _p = prefix + to_string(get_combined_id(process_id, thread_id)) + "/";
                mkdir((_p + "2").c_str(), 0);
                mkdir((_p + "2/3").c_str(), 0);
                mkdir((_p + "2/3/4").c_str(), 0);
                int fd = open((_p + "2/3/4/test").c_str(), O_CREAT | O_RDWR);
                if (fd > 0)
                    close(fd);
            }
        }
#elif mode == MODE_SINGLE_FILE
        mkdir((prefix + "1").c_str(), 0);
        mkdir((prefix + "1/2").c_str(), 0);
        mkdir((prefix + "1/2/3").c_str(), 0);
        mkdir((prefix + "1/2/3/4").c_str(), 0);
        close(open((prefix + "1/2/3/4/test").c_str(), O_CREAT | O_RDWR));
#endif
    };

    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings)
    {
        int fd;
        struct stat64 aaa;

#if mode == MODE_SHARED_DIR
        string path = prefix + "1/2/3/4/" + to_string(get_combined_id(process_id, thread_id));
#elif mode == MODE_PRIVATE_DIR
        string path = prefix + to_string(get_combined_id(process_id, thread_id)) + "/2/3/4/test";
#elif mode == MODE_SINGLE_FILE
        string path = prefix + "1/2/3/4/test";
#endif

        for (size_t c = 0; c < current_op_count; c++)
        {
            // fd = open(path.c_str(), O_RDWR);
            // if (fd < 0){
            //     cout << "fsdfsdfsdf" << endl;
            // }
            // else {
            //     close (fd);
            // }   
            lstat64(path.c_str(), &aaa);
        }

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