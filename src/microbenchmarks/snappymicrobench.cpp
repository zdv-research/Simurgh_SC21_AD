#include "benchmark_base.hpp"

#include <unistd.h>
#include <fcntl.h>


#include "snappy/snappy.h"


#define COMPRESS 0
#define UNCOMPRESS 1
#ifndef bytes_per_op
#define bytes_per_op 128*1024
#endif

#ifndef op_count
#define op_count 128*1024
#endif

#ifndef mode
#define mode COMPRESS
#endif

// TODO: make this benchmark MP ready: prepare->prepare_once and add prepare_per_process

class concrete_benchmark : public benchmark_base {
public:
    concrete_benchmark()
    {
#if mode == UNCOMPRESS
        set_title("snappy_benchmark");
#elif mode == COMPRESS
        set_title("snappy_benchmark");
#endif
    };

#if bytes_per_op == 4096
    static const size_t distribute = 20000;
#else
    static const size_t distribute = 50;
#endif

    vector<int> read_preloaded_fds;
    vector<int> write_preloaded_fds;
    char initdata[bytes_per_op];
    char testdata[2][bytes_per_op];
    char t_readbuffer[20][bytes_per_op];
    char t_compressedbuffer[20][2446709];
    size_t output_length, input_length;
   // unsigned long long op_count, total;
    //struct snappy_env *env;
    

    void print (const benchmark_settings &settings) {
        cout << "testdata: ";
        for (int i = 0; i < bytes_per_op; i++)
            cout << testdata[i];
        cout << endl;

        for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++) {
            cout << "t_readbuffer " << thread_id << " :";
            for (int i = 0; i < bytes_per_op; i++)
                cout << t_readbuffer[thread_id][i];
            cout << endl;
            cout << "t_compressedbuffer " << thread_id << " :";
            for (int i = 0; i < output_length; i++)
                cout << t_compressedbuffer[thread_id][i];        
            cout << endl;

        }
    }

    virtual void prepare(const benchmark_settings &settings) {
        cout << "total file count " << op_count << endl; 
        input_length = bytes_per_op;
        cout << "bytes per op " << bytes_per_op << endl;
        output_length = snappy_max_compressed_length(input_length);
        //cout << "output lenght" << output_length << endl ;
        for (size_t i = 0; i < bytes_per_op; i++) {
            testdata[0][i] = 'a';
            testdata[1][i] = 'b';
            initdata[i] = (char) ((((i+i)*i) % 255) + 1);
            
        }

    for (size_t process_id = 0; process_id < settings.process_count; process_id++) {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++) {
                string p1 = prefix + to_string((process_id+1 << 4) + thread_id+1) + "_";

                for (int i = 0; i < settings.operation_per_thread_count; i++) {
                    string p = p1 + to_string(i);

                    int fd = open(p.c_str(), O_CREAT | O_RDWR);
                    write(fd, initdata, bytes_per_op);
                    if (fd > 0) 
                        close(fd);
                }
            }
        }
    };


    virtual void run_managed(int current_op_count, int process_id, int thread_id, const benchmark_settings &settings) {
        //cout << "inside run managed \n";
        int combined_id = process_id * settings.thread_per_process_count + thread_id;

#if mode == UNCOMPRESS
        cout << "current_op_count " << current_op_count << endl;
        int fd = preloaded_fds[thread_id];
        for (size_t j = 0; j < current_op_count; j++)
        {
            pwrite(fd, testdata[j%2], bytes_per_op, (combined_id + j%distribute) * bytes_per_op);
            fsync(fd);
        }

#elif mode == COMPRESS

        string p1 = prefix + to_string((process_id+1 << 4) + thread_id+1) + "_";
        string p2 = prefix + to_string((process_id+1 << 4) + thread_id+1) + "c_";
        struct snappy_env env[current_op_count];
        for (int i = 0; i < current_op_count; i++) {
            snappy_init_env(&env[i]);
            string up = p1 + to_string(i);
	    string cp = p2 + to_string(i);
            int ufd = open(up.c_str(), O_RDWR);
	    //cout << "read fd number " << ufd << endl;
            ssize_t rerr = pread(ufd, t_readbuffer[thread_id], bytes_per_op, 0);
	    //cout << "read bytes " << rerr << endl;
            int cfd= open(cp.c_str(), O_CREAT | O_RDWR);
	    //cout << "write fd number" << cfd << endl;
            int ret = snappy_compress(&env[i], t_readbuffer[thread_id], input_length, t_compressedbuffer[thread_id], &output_length);
            //cout << "compress " << ret << endl;
            ssize_t errw = pwrite(cfd,t_compressedbuffer[thread_id], output_length, 0);
           // cout << "compressed size " << errw << endl;

            fsync(cfd);
            fsync(ufd);
            close(ufd);
            close(cfd);
        }

#endif
    };

    virtual bool test(const benchmark_settings &settings) {

#if mode == UNCOMPRESS

        for (size_t process_id = 0; process_id < settings.process_count; process_id++) {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++) {
                
                for (size_t j = 0; j < settings.operation_per_thread_count; j++)
                {
                    int fd = preloaded_fds[thread_id];
                    pread(fd, t_readbuffer[thread_id], bytes_per_op, (thread_id*settings.thread_per_process_count + process_id) * bytes_per_op);
                }

            }
        }

        for (size_t process_id = 0; process_id < settings.process_count; process_id++) {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++) {
                
                for (size_t j = 0; j < bytes_per_op; j++) {
                    if (t_readbuffer[thread_id][j] != 'a')
                        return false;
                }

            }
        }

#elif mode == COMPRESS

        for (size_t process_id = 0; process_id < settings.process_count; process_id++) {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++) {
                
                for (size_t j = 0; j < bytes_per_op; j++) {
                    if (t_readbuffer[thread_id][j] == 0 || t_compressedbuffer[thread_id][j] ==0)
                        return false;
                }

            }
        }
        for (size_t process_id = 0; process_id < settings.process_count; process_id++) {
            for (size_t thread_id = 0; thread_id < settings.thread_per_process_count; thread_id++) {
                
                string p2 = prefix + to_string((process_id+1 << 4) + thread_id+1) + "c_";
                for (int i = 0; i < settings.operation_per_thread_count; i++) {
                    string p=p2+to_string(i);

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

void setup (benchmark_base*& benchmark) {
    benchmark = new concrete_benchmark();
};
