#!/bin/bash

umount /mnt/fsramdisk
rm -rf /mnt/fsramdisk/*
umount /mnt/pmem_emul
rm -rf /mnt/pmem_emul/*