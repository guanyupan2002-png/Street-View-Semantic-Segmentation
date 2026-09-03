# Street-View Semantic Segmentation — FAST V2 BALANCED

Batch semantic segmentation for street-view imagery using a hybrid pipeline based on:

- SegFormer B5 (ADE20K)
- Mask2Former (Mapillary Vistas)
- Grounding DINO
- SAM2

The FAST V2 BALANCED runner preserves the v1.5.7.1 taxonomy and the main fusion/refinement logic while reducing Grounding DINO overhead by batching same-purpose crops/ROIs. Mixed precision is used for DINO/SAM in the fast mode, so results are intended to remain visually close to the audited baseline, not bit-identical.

## Repository structure

```text
Street-View-Semantic-Segmentation/
├── segmentation_colab.ipynb
├── segmentation_local.py
├── requirements.txt
├── README.md
├── .gitignore
├── config.example.json
├── run_windows_test.bat
└── example_input/
    └── README.md
```

## Outputs

For every successfully processed image, the runner creates:

```text
outputs/
├── summary_images/
├── label_maps/
├── audit_outputs/
├── segmentation_results.csv
└── errors.csv
```

`segmentation_results.csv` contains one row per image, including per-class percentages.

Percentages are calculated over valid non-IGNORE pixels. Google Street View UI/artifact regions assigned to `IGNORE=255` are excluded from the denominator. `bike_lane` is merged into `roadway` in the final user-facing output.

## 30-class taxonomy

The pipeline declares these classes:

`other_unknown`, `roadway`, `sidewalk`, `bike_lane`, `curb_edge`,
`upper_building_facade`, `ground_floor_solid_facade`,
`ground_floor_glazing`, `door_entrance`, `signboard`, `awning_canopy`,
`arcade_column`, `arcade_soffit`, `sidewalk_shed_scaffold`,
`stoop_stair`, `wall_ledge`, `fence_railing`, `planter_container`,
`tree`, `shrub_hedge`, `ground_vegetation`, `vertical_green_wall`,
`bench_seating`, `pole_fixture`, `traffic_sign_signal`, `person`,
`vehicle`, `sky`, `upper_building_glazing`, `traffic_cone_barrel`.

## Option A — Google Colab

1. Upload `segmentation_colab.ipynb` to Colab.
2. Select a GPU runtime.
3. Run the notebook.
4. In the **USER CONFIGURATION** cell, edit only:

```python
DRIVE_PROJECT_DIR = Path("/content/drive/MyDrive/StreetViewSegmentation")
MAX_IMAGES = 3
```

5. Put input images in:

```text
My Drive/
└── StreetViewSegmentation/
    └── input_images/
```

6. First run 3 images. After validating speed and output, change:

```python
MAX_IMAGES = None
```

`RESUME = True` is enabled by default, so completed images are skipped on later runs.

## Option B — Windows / local NVIDIA GPU

Recommended: Python 3.11 and an NVIDIA CUDA-capable GPU.

Create:

```text
your_project/
├── segmentation_local.py
├── input_images/
└── outputs/
```

Install a CUDA-enabled PyTorch build appropriate for your machine first. Example only:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

Then install the remaining dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python segmentation_local.py
```

The local runner defaults to relative folders:

```python
INPUT_DIR = Path("./input_images")
BATCH_OUTPUT_ROOT = Path("./outputs")
MAX_IMAGES = 3
```

After validating the first test:

```python
MAX_IMAGES = None
```

### GPU memory handling

The local runner automatically checks GPU VRAM.

- Under 12 GB VRAM: `LOW_VRAM_MODE = True`
- 12 GB or more: it first tries keeping all models resident on the GPU
- If CUDA runs out of memory, it falls back to low-VRAM mode

Low-VRAM mode is safer but can be slower because models are moved between CPU RAM and GPU memory.

## Large-batch note

The code is designed for 10,000+ images and supports resume, incremental CSV writing, and error logging. Runtime depends strongly on GPU, image resolution, storage speed, and whether low-VRAM mode is active.

A 48-hour target for 10,000 images requires an average throughput of approximately **17.28 seconds/image**. Benchmark on your own hardware before committing to a production deadline.

## Supported image formats

`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tif`, `.tiff`

## Model downloads

Model weights are not stored in this repository. They are downloaded automatically from Hugging Face on first run.

Model IDs:

```text
nvidia/segformer-b5-finetuned-ade-640-640
facebook/mask2former-swin-large-mapillary-vistas-semantic
IDEA-Research/grounding-dino-base
facebook/sam2.1-hiera-small
```

Users should review and comply with the licenses/terms of the upstream models and datasets.

## Do not commit

Do not upload these to GitHub:

- street-view image datasets
- model weight/cache folders
- generated result folders
- CSV outputs containing project data
- API keys or Hugging Face tokens
- local virtual environments

The included `.gitignore` excludes common large/generated files.

## Reproducibility note

FAST V2 uses batched Grounding DINO crops and optional FP16 inference for DINO/SAM. Borderline detections can therefore differ slightly across GPU types, CUDA/PyTorch versions, or precision settings. Treat this as a close-output production mode rather than a bit-exact reproduction mode.

## Recommended team workflow

Each team member should clone the same repository and keep their own `input_images/` and `outputs/` folders locally or in their own Drive. Do not commit generated outputs unless the team explicitly decides to version a small validation sample.
