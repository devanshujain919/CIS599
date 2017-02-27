for i in $(seq 0 99)
do
    cd shard/shard-$i
    qsub -cwd run.sh
    cd -
done
