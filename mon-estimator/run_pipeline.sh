default_output="data"

if [ -z "$1" ]
  then
    echo "Input images folder required"
    echo "run_pipeline.sh <input-folder> <json-configuration> <output-tex>"
    exit 1
fi

if [ -z "$2" ]
  then
    echo "Expected JSON configuration"
    echo "run_pipeline.sh <input-folder> <json-configuration> <output-tex>"
    exit 1
fi

if [ -z "$3" ]
  then
    echo "Output figure LaTeX file"
    echo "run_pipeline.sh <input-folder> <json-configuration> <output-tex>"
    exit 1
fi


input=$1
jsonfile=$2
outputfile=$3

echo "============================================"
echo "[Step 1] data extraction"
echo "============================================"
echo "Prepare images with border..."

python mon-estimator/run/prepare_image_multiple.py --folder $input --json $jsonfile --method border --output $outputfile/border

echo "Prepare cropped images..."
python mon-estimator/run/prepare_image_multiple.py --folder $input --json $jsonfile --method crop --output $outputfile/crop

echo "============================================"
echo "[Step 2] images comparisons"
echo "============================================"

python mon-estimator/run/compare_image_multiple.py --folder data/$outputfile --json $jsonfile --output data/$outputfile/metrics

echo "============================================"
echo "[Step 3] build of LaTeX figure"
echo "============================================"

python mon-estimator/run/build_figure.py --folder data/$outputfile/metrics --json $jsonfile --output data/$outputfile.tex