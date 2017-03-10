for i in $(seq 0 9)
do
    for j in $(seq 60 10 90)
    do
        echo "run_$3/rep-$i/train-$j"
        cd "run_$3/rep-$i/train-$j"
        file="data/test/corpus.$1"
        scriptfile="test/1/model/run-joshua.sh"
        options="-m 4g -threads 1 -top-n $2 -output-format \"%i ||| %s\""
        outputfile="test/output-top-$2"
        logfile="test/joshua-top-$2.log"
        echo "cat $file | $scriptfile $options >$outputfile 2>$logfile"
        echo "cat $file | $scriptfile $options >$outputfile 2>$logfile" > decode-top-$2.sh
        qsub -cwd decode-top-$2.sh
        cd -
    done
done

