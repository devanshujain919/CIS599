echo "Will evaluate for top $1 transliterations"

rm -r result
mkdir result
for j in $(seq 60 10 90)
do
    echo "Avg Normalised Edit Distance, Accuracy, F-Score, MRR, MAP" >> result/train-$j
    echo "---------------------------------------------------------" >> result/train-$j
    for i in $(seq 0 9)
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

for i in $(seq 60 10 90)
do
    echo "train-$i"
    awk '
        BEGIN{
            FS=", "; 
            ORS=" " ; 
            for(i=1;i<=NF;i++) 
                total[i]=0; 
            count = 0;
        } 
        NR>2{ 
            for(i=1;i<=NF;i++) 
                total[i] += $i; 
            count ++;
        } 
        END{
            print "---------------------------------------------------------\n"
            for(i=0;i<=NF;i++)
                print total[i]/count; 
        }
    ' result/train-$i >> result/train-$i
done
