#!/bin/bash

### displays images using fbi ###

txt_files_dir="/home/pi/random_lists/"

# Optionally, execute python script:
# python3 /home/pi/images/generate_random_lists.py --source_dir /home/pi/images/ --target_dir $txt_files_dir

cachemem=10 # in MB
blend=100   # in milliseconds (transition time between images)
timeout=3.5 # in seconds

while true; do
    # file lists are saved as txt files in txt_files_dir, so pick a random one using find
    random_file_list=$(find $txt_files_dir -type f -name "*.txt" | shuf -n 1)

    # (autozoom to fit screen, no verbose output, random order, read ahead into cache (10MB),
    # blend images (0.1 second transition), virtual console 1, timeout 3.5 seconds)
    sudo fbi --autozoom -noverbose --random --readahead --cachemem $cachemem --blend $blend -T 1 --timeout $timeout --once --list $random_file_list &>/dev/null

    # Wait for fbi process to finish
    wfp=$(pidof fbi)
    while sudo kill -0 $wfp >/dev/null 2>&1; do
        sleep 5
    done
done