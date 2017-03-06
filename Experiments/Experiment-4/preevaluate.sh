for i in $(seq 0 9)
do
    for j in $(seq 60 10 90)
    do
        echo "run/rep-$i/train-$j"
        cd "run/rep-$i/train-$j/source-intermediate/"
        rm decode-top-*
        file="../input/test.hi"
        scriptfile="test/1/model/run-joshua.sh"
        options="-m 4g -threads 1 -top-n $1 -output-format \"%i ||| %s\""
        outputfile="test/output-top-$1"
        logfile="test/joshua-top-$1.log"
        echo "cat $file | $scriptfile $options >$outputfile 2>$logfile"
        echo "cat $file | $scriptfile $options >$outputfile 2>$logfile" > decode-top-$1.sh
        qsub -cwd decode-top-$1.sh
        cd -
    done
done

