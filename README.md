# medimage-qc

A lightweight NIfTI quality-check script I wrote while learning
how medical imaging data is represented and processed.

## Background

In my second year, Prof. Ramesh Saha asked me to run a segmentation
model on a small kidney dataset as part of a lab task. That was my
first real encounter with NIfTI files — I had no idea what a voxel
grid was or why intensity histograms looked so inconsistent across
scans. After the task was done I kept poking at the data: I wanted
to understand what "a good scan" even looks like before a model
touches it.

This script is the result of that curiosity. It does three things:

1. Reports basic intensity statistics on foreground voxels
2. Estimates a simple SNR (signal-to-noise ratio)
3. Saves an axial-slice montage so you can eyeball the volume

That's it. No preprocessing, no pipeline — just enough to sanity-check
a NIfTI file before you hand it to something more sophisticated.

## Usage

```bash
pip install -r requirements.txt
python qc_check.py path/to/volume.nii.gz
```

Output: printed stats in the terminal + a `*_montage.png` saved next
to the input file.

## What I Learned

- NIfTI header metadata (affine, voxel dimensions, data dtype)
- Why raw intensity ranges vary so wildly across scanners
- How to navigate 3-D numpy arrays and visualise volumetric slices
- The difference between image-level QC and model-level evaluation

## What This Is Not

This is not a clinical pipeline. It does not anonymise DICOM files,
run bias-field correction, perform skull stripping, or containerise
anything. If you need that, look at tools like
[mriqc](https://mriqc.readthedocs.io/) or
[fmriprep](https://fmriprep.org/).
