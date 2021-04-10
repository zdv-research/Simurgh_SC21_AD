for n in $(find $1/*.txt); do echo $n >> average_$1.txt; grep Summary $n | tail -n5 | cut -d" " -f6 | awk '{ total += $1; count++ } END { print total/count }' >> average_$1.txt; done
