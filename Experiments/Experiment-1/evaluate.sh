echo "Will evaluate for top $1 transliterations"

rm -r result
mkdir result
for i in $(seq 0 9)
do
    for j in $(seq 60 10 90)
    do
        echo "rep-$i/train-$j"
        rm output
        cat run/rep-$i/train-$j/test/output-top-$1 > output
        rm true
        cat run/rep-$i/train-$j/input/test.en > true
        python evaluations.py -t true -e output -n $1 >> result/train-$j
        rm output
        rm true
    done
done

#for i in $(seq 60 10 90)
#do
#    echo "train-$i"
#    awk '{ total += $1; count++ } END { print total/count }' result/train-$i
#done
