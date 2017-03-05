for i in $(seq 0 99)
do
    cp createData.py shard/shard-$i/
    cd shard/shard-$i
    rm run_create_data.sh*
    echo "python createData.py -i wiki-shard.txt -d data/ -m ne_filename.txt -n nationalities.txt -o wiki-shard.json" >> run_create_data.sh 
    qsub -cwd run_create_data.sh
    cd -
done

