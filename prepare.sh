#!/bin/bash

wget --show-progress -P data https://seafile.rlp.net/f/a63db23c264a4258bd1d/?dl=1 
mv data/index.html?dl=1 data/linux.tar

mkdir -P leveldb/workloads

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/814e27fe438c4168951d/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/loada_5M

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/1f8216bd42bd432b9970/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/loade_5M

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/e9e9158faaa942aca814/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/runa_5M_5M

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/527fa1cd24db47509b50/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/runb_5M_5M

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/3cc6ed7cf785494b9e1a/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/runc_5M_5M

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/1431c80c8fbc4c8cac86/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/rund_5M_5M

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/d8915849c95b4c0cbc32/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/rune_5M_1M

wget --show-progress -P leveldb/workloads https://seafile.rlp.net/f/bc2a9ce5a9944c7a8d84/?dl=1
mv leveldb/workloads/index.html?dl=1 leveldb/workloads/runf_5M_5M

wget --show-progress -P data https://seafile.rlp.net/f/57c31d7fa4954b8eb4eb/?dl=1
yes | mv data/index.html?dl=1 data/ycsb.tar.gz
tar -xzf data/ycsb.tar.gz -C data/