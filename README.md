## Repository Notes

To keep the repository lightweight, large datasets and generated outputs are not included.

The following files should remain local:
- Street-view image datasets
- Generated segmentation results
- Model weights and cache files
- Local virtual environments

Model weights are downloaded automatically from Hugging Face when the pipeline is first executed.

## Reproducibility

FAST V2 uses batched Grounding DINO inference and FP16 inference for DINO and SAM2 to improve processing speed.

Because results may vary slightly across GPU models, CUDA versions, and PyTorch versions, outputs from different computers are expected to be visually similar but may not be pixel-identical.

## Team Workflow

Each team member can clone this repository and run the same segmentation pipeline on their own computer or Google Colab.

Keep input images and generated outputs locally:

input_images/ → Street-view images  
outputs/ → Segmentation results
