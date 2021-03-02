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

### Images conversion

If necessary to convert images into `png` file format:
```bash
python mon-estimator/run/convert_to_png.py --folder <rawls-images-folder> --output <png-images-folder>
```

### Prepare all images

```bash
python mon-estimator/run/prepare_image_multiple.py --json <figure_build.json> --method <crop | border>
```

- `<figure_build.json>`: example is available into [json](json/figure_build.example.json) folder.

**Note:** generated image data will be saved into `data` default folder.

### Compare all images

Compare the generated folder into `.csv` files:
```bash
python mon-estimator/run/compare_image_multiple.py --json <figure_build.json>
```

### Build LaTeX figure

Then build the figure:

```bash
python mon-estimator/run/build_figure.py --json <figure_build.json> --output data/<generated-figure.tex>
```

## Prepare all data

```bash
bash mon-estimator/run_pipeline.sh <png-input-folder> <json-configuration> <output-tex>
```

**Note:** this step requires at least `png` images conversion.