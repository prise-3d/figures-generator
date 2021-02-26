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
echo "[Step 0] data processing with nsamples"
echo "============================================"
echo "Prepare folder with specific nsamples..."

python mon-estimator/run/create_nsamples_folder.py --folder $input --json $jsonfile

echo "============================================"
echo "[Step 1] data extraction"
echo "============================================"
echo "Prepare images with border..."

python mon-estimator/run/prepare_image_multiple.py --json $jsonfile --method border

echo "Prepare cropped images..."
python mon-estimator/run/prepare_image_multiple.py --json $jsonfile --method crop

echo "============================================"
echo "[Step 2] images comparisons"
echo "============================================"

python mon-estimator/run/compare_image_multiple.py --json $jsonfile

echo "============================================"
echo "[Step 3] build of LaTeX figure"
echo "============================================"

python mon-estimator/run/build_figure.py --json $jsonfile --output data/$outputfile.tex