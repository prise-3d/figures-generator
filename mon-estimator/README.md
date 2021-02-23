# MON-Estimator

## Expected images folder structure

```console
.                                    || 
├── reference                        || folder with references images of each scene
│   └── ...                          || specific scene sub-folders with one image (the reference one)
├── estimator1                       || first estimator to compare
│   └── ...                          || specific scene sub-folders with some generated images with samples
├── estimator2                       || second estimator to compare
│   └── ...                          || specific scene sub-folders with some generated images with 
├── ...                              || Others estimators
```

with the following images filename convention:

```
p3d_<scene-name>-S<nsamples>-<index>.<extension>
```
## Usage

## Images conversion

If necessary to convert images into `png` file format:
```bash
python mon-estimator/run/convert_to_png.py --folder <rawls-images-folder> --output <png-images-folder>
```

## Prepare all images

```bash
python mon-estimator/run/prepare_image_multiple.py --folder <png-images-folder> --json <figure_build.json> --method <crop | border> --output <prepared-images-folder>/<method>
```

- `<prepare_image.json>`: example is available into [json](json/figure_build.json) folder.

**Note:** generated image data will be saved into `data` default folder.

## Compare all images

Compare the generated folder into `.csv` files:
```bash
bash mon-estimator/run/compare_all.sh <prepared-images-folder> <output-metrics> <reference-estimator>
```

## Build LaTeX figure

Then build the figure:

```bash
python mon-estimator/run/build_figure.py --folder <output-metrics> --prefix <prefix> --json <figure_build.json> --output <generated-figure.tex>
```