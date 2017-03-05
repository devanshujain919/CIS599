for i in $(seq 0 99)
do
    cp find-nationality.perl shard/shard-$i/
    cd shard/shard-$i/
    find data/articles/en -print0 | xargs -0 perl find-nationality.perl >nationalities.txt
    cd -
done
