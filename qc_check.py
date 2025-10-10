"""
medimage-qc — basic NIfTI quality checks
Loads a NIfTI volume, reports intensity statistics and SNR,
and saves a montage of axial slices for visual inspection.
"""

import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def load_volume(path: str):
    img = nib.load(path)
    data = img.get_fdata()
    return img, data


def intensity_stats(data: np.ndarray) -> dict:
    flat = data[data > 0]          # ignore background voxels
    return {
        "min":    float(flat.min()),
        "max":    float(flat.max()),
        "mean":   float(flat.mean()),
        "std":    float(flat.std()),
        "median": float(np.median(flat)),
    }


def estimate_snr(data: np.ndarray) -> float:
    """
    Simple foreground-mean / background-std SNR estimate.
    Threshold at 10 % of max to separate foreground from background.
    """
    threshold = data.max() * 0.10
    signal = data[data > threshold].mean()
    noise  = data[data <= threshold].std()
    return float(signal / noise) if noise > 0 else float("inf")


def save_slice_montage(data: np.ndarray, out_path: str, n_slices: int = 9):
    """Save a grid of evenly-spaced axial slices."""
    z_total = data.shape[2]
    indices = np.linspace(z_total * 0.1, z_total * 0.9, n_slices, dtype=int)

    fig = plt.figure(figsize=(15, 5))
    gs  = gridspec.GridSpec(1, n_slices, wspace=0.05)

    for col, z in enumerate(indices):
        ax = fig.add_subplot(gs[col])
        ax.imshow(data[:, :, z].T, cmap="gray", origin="lower")
        ax.set_title(f"z={z}", fontsize=7)
        ax.axis("off")

    fig.suptitle("Axial slice montage", fontsize=10)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Montage saved → {out_path}")


def run_qc(nifti_path: str):
    print(f"\n── medimage-qc ──────────────────────────")
    print(f"File : {nifti_path}")

    img, data = load_volume(nifti_path)
    print(f"Shape: {data.shape}   Voxel size: {img.header.get_zooms()}")

    stats = intensity_stats(data)
    print("\nIntensity statistics (foreground voxels):")
    for k, v in stats.items():
        print(f"  {k:>8}: {v:.2f}")

    snr = estimate_snr(data)
    print(f"\nSNR estimate : {snr:.2f}")

    out_png = nifti_path.replace(".nii.gz", "").replace(".nii", "") + "_montage.png"
    save_slice_montage(data, out_png)
    print("─────────────────────────────────────────\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qc_check.py <path/to/volume.nii.gz>")
        sys.exit(1)
    run_qc(sys.argv[1])
