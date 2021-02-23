reference="reference"

if [ -z "$1" ]
  then
    echo "No argument supplied for images folder"
    exit 1
fi

if [ -z "$2" ]
  then
    echo "No argument supplied for output folder metrics"
    exit 1
fi

if [ -z "$3" ]
  then
    echo "References estimator not supplied"
    exit 1
fi

folder="$(pwd)"/$1
output="$(pwd)"/$2
reference=$3

counter=0

if [ ! -d "$output" ]; then
  echo "Creation of output folder..."
  mkdir $output
fi

for method in {"border","crop"};
do
    for est in {"mean","mean-or-mon","mon","amon","reference"};
    do
        # generate str index
        length=$(expr length "$counter")
        stop=$((3 - length))
        
        counterstr="$counter"
        for i in $(seq 0 $stop)
        do
            counterstr="0$counterstr"
        done

        python mon-estimator/run/compare_image_multiple.py --folder "${folder}/${method}" --estimators "${reference},${est}" --method rmse --output "${output}/${counterstr}_${method}_${reference}_${est}.csv"

        counter=$((counter + 1))
    done
done