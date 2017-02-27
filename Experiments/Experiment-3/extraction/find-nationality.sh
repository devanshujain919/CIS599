for i in $(seq 0 99)
do
    cp find-nationality.perl shard/shard-$i/
    cd shard/shard-$i/
    cat ne_filename.txt | cut -f 2 | grep "data\/articles\/en" | xargs perl find-nationality.perl > nationalities.txt
    cd -
done
