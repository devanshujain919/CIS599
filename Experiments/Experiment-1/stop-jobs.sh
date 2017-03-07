for i in $(seq 0 9)
do
    for j in $(seq 60 10 90)
    do
        cd "run/rep-$i/train-$j"
        ls run.sh.e* | cut -d "." -f 3 | sed 's/^e//g' | xargs qdel 
        cd -
    done
done
