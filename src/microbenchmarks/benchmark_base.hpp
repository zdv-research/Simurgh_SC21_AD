#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <vector>

#include "cxxopts.hpp"
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>
       
using namespace std;
using ns = chrono::nanoseconds;
using get_time = chrono::steady_clock;

struct benchmark_settings
{

    // set in base
    int operation_count = 100;
    int thread_per_process_count = 1;
    int process_count = 1;
    int operation_per_process_count = 100;
    int operation_per_thread_count = 100;
    int process_id = 0;
    bool long_file_names = false;
    bool use_temp_dir = false;
    bool drop_caches = true;
    bool only_prepare_run = false;
    bool only_measurement_run = false;
    bool only_postpare_run = false;
    string root;

    // set in derived
    bool do_test = false;
    bool do_cleanup = false;
    bool run_manual = false;
};

class benchmark_base
{
public:

    virtual void do_custom_settings(benchmark_settings& settings, cxxopts::ParseResult& result) {};
    virtual void prepare(const benchmark_settings& settings) {};
    virtual void prepare_on_measurement(const benchmark_settings& settings) {};
    virtual void postpare_on_measurement(const benchmark_settings& settings) {};
    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings& settings) {};
    virtual void run_manual(const benchmark_settings& settings) {};
    virtual bool test(const benchmark_settings& settings)
    {
        return true;
    };
    virtual void cleanup(const benchmark_settings& settings) {};

    void startup(cxxopts::ParseResult& result, benchmark_settings& settings)
    {
        this->settings = settings;
        do_custom_settings(settings, result);

        prefix = get_filename_prefix();

        settings.operation_per_process_count = settings.operation_count / settings.process_count;
        settings.operation_per_thread_count = settings.operation_per_process_count / settings.thread_per_process_count;
    }

    void prepare_benchmark(cxxopts::ParseResult& result, benchmark_settings& settings)
    {
        cout << endl;
        cout << "Prepare benchmark: " << title << endl;
        cout << "  - operation_count: " << settings.operation_count << endl;
        cout << "  - thread_per_process_count: " << settings.thread_per_process_count << endl;
        cout << "  - process_count: " << settings.process_count << endl;
        cout << "  - operation_per_process_count: " << settings.operation_per_process_count << endl;
        cout << "  - operation_per_thread_count: " << settings.operation_per_thread_count << endl;
        cout << "  - prefix: " << prefix << endl;

        prepare(settings);

        if (settings.drop_caches)
            drop_caches();

        cout << "Benchmark preparation done." << endl;
    }

    void do_measurement(cxxopts::ParseResult& result, benchmark_settings& settings)
    {

        reset_timings();

        prepare_on_measurement(settings);

        if (settings.run_manual)
        {
            // currently not needed, but if, this needs proper time measurement
            // run_manual(settings);
        }
        else
        {

            vector<thread> threads;
            threads.reserve(settings.thread_per_process_count);

            for (size_t i = 0; i < settings.thread_per_process_count; i++)
                threads.push_back(thread([i, &settings, this]()
            {
                auto start_t = get_time::now();

                run_managed(settings.operation_per_thread_count, settings.process_id, i, settings);

                auto end_t = get_time::now();
                auto diff = end_t - start_t;
                auto diff_ns = chrono::duration_cast<ns>(diff).count();
                this->timings[i] = diff_ns;
            }));

            for (size_t i = 0; i < settings.thread_per_process_count; i++)
                threads[i].join();

            cout << "Time: " << (get_max_timing()) / 1000000. << " ms" << endl;
        }

        postpare_on_measurement(settings);

    }

    void postpare_benchmark(cxxopts::ParseResult& result, benchmark_settings& settings)
    {

        cout << "Postpare benchmark." << endl;

        if (settings.do_test)
        {
            bool success = test(settings);
            if (success)
            {
                cout << "Benchmark test successfull." << endl;
            }
            else
            {
                cout << "Benchmark test error." << endl;
            }
        }

        if (settings.do_cleanup)
        {
            cleanup(settings);
            cout << "Cleanup done." << endl;
        }

        cout << "Benchmark finished!" << endl;
        cout << endl;
    }

    void execute(cxxopts::ParseResult& result, benchmark_settings& settings)
    {
        startup(result, settings);

        if (settings.process_count == 1)
        {
            prepare_benchmark(result, settings);
            cout << "Start run ..." << endl;
            do_measurement(result, settings);
            postpare_benchmark(result, settings);
        }
        else
        {
            if (settings.only_measurement_run)
                do_measurement(result, settings);
            else if (settings.only_prepare_run)
                prepare_benchmark(result, settings);
            else if (settings.only_postpare_run)
                postpare_benchmark(result, settings);
        }


    };

protected:

    string prefix;

    string get_filename_prefix()
    {
        // string filename_prefix_short_root = "/pm:";
        // string filename_prefix_short_temp_dir = "temp/pm:";
        // string filename_prefix_long_root = "/pm:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"; // 128 chars
        // string filename_prefix_long_temp_dir = "temp/pm:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"; // 128 chars

        // if (settings.long_file_names) {
        //     if (settings.use_temp_dir) {
        //         return filename_prefix_long_temp_dir;
        //     } else {
        //         return filename_prefix_long_root;
        //     }
        // } else {
        //     if (settings.use_temp_dir) {
        //         return filename_prefix_short_temp_dir;
        //     } else {
        //         return filename_prefix_short_root;
        //     }
        // }
        return settings.root;
    };

    void set_title(string title)
    {
        this->title = title;
    };

    size_t get_combined_id(size_t process_id, size_t thread_id)
    {
        return process_id * settings.thread_per_process_count + thread_id;
    }

private:
    benchmark_settings settings;
    int64_t timings[256];
    string title = "no_title";

    void reset_timings()
    {
        for (size_t i = 0; i < 256; i++)
        {
            timings[i] = 0;
        }
    };

    int64_t get_max_timing()
    {
        int64_t max = 0;
        for (size_t i = 0; i < 256; i++)
        {
            if (timings[i] > max)
            {
                max = timings[i];
            }
        }
        return max;
    };

    void drop_caches()
    {
        system("bash -c 'sync; echo 3 > /proc/sys/vm/drop_caches;'");
    };

};

benchmark_base* benchmark;
extern void setup(benchmark_base*& benchmark);

int main(int argc, char** argv)
{

    setup(benchmark);

    cxxopts::Options options("create_file_test", "");
    options.add_options()
    ("root", "root", cxxopts::value<string>())
    ("process_id", "process_id", cxxopts::value<int>())
    ("processes", "process amount", cxxopts::value<int>())
    ("t,threads", "thread amount", cxxopts::value<int>())
    ("operations", "operations", cxxopts::value<int>())
    ("drop_caches", "drop_caches", cxxopts::value<int>())
    ("do_checks", "do_checks", cxxopts::value<int>())
    ("only_prepare_run", "only_prepare_run", cxxopts::value<int>())
    ("only_measurement_run", "only_measurement_run", cxxopts::value<int>())
    ("only_postpare_run", "only_postpare_run", cxxopts::value<int>());
    options.allow_unrecognised_options();
    cxxopts::ParseResult result = options.parse(argc, argv);

    benchmark_settings settings;

    if (result.count("root"))
        settings.root = result["root"].as<string>();
    if (result.count("process_id"))
        settings.process_id = result["process_id"].as<int>();
    if (result.count("processes"))
        settings.process_count = result["processes"].as<int>();
    if (result.count("threads"))
        settings.thread_per_process_count = result["threads"].as<int>();
    if (result.count("operations"))
        settings.operation_count = result["operations"].as<int>();
    if (result.count("drop_caches"))
        settings.drop_caches = result["drop_caches"].as<int>();
    if (result.count("do_checks"))
        settings.do_test = result["do_checks"].as<int>();
    if (result.count("only_prepare_run"))
        settings.only_prepare_run = result["only_prepare_run"].as<int>();
    if (result.count("only_measurement_run"))
        settings.only_measurement_run = result["only_measurement_run"].as<int>();
    if (result.count("only_postpare_run"))
        settings.only_postpare_run = result["only_postpare_run"].as<int>();

    benchmark->execute(result, settings);

    return 0;
};

// Helpers

inline string generate_filename(string& prefix, int process_id, int thread_id, int number)
{
    return prefix + to_string((int)((1 << 30) + (process_id << 24) + (thread_id << 16) + number));
}

inline void call_dummy_system_call() {
    syscall(999991);
    // pid_t tid;
    // tid = syscall(SYS_gettid);
    //pid_t p = getpid();
}
