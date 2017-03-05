for i in $(seq 0 99)
do
    cp backlink-extractor-2.py shard/shard-$i/
    cd shard/shard-$i
    rm run_back.sh*
    echo "python backlink-extractor-2.py wiki-shard.txt" >> run_back.sh 
    qsub -cwd run_back.sh
    cd -
done
