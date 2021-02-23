reference="reference"
folder="/home/jbuisine/Downloads/mon_study"
output="/home/jbuisine/Downloads/mon_study/metrics/"

for method in {"crop","border"};
do
    for est in {"reference","mean","mon","mean-or-mon","amon"};
    do
        python run/compare_image_multiple_v2.py --folder "${folder}/${method}" --estimators "${reference},${est}" --method rmse --output "${output}/${method}_${reference}_${est}.csv"
    done
done