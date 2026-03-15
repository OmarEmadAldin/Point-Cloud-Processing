# Point Cloud Subsampling

Two classic strategies for reducing point cloud density — implemented in Python using `laspy` and `open3d`.

---

## Methods

### Decimation
Keep every **N-th point** from the original array. Simple, fast, and order-dependent.

```
Original:  ● ● ● ● ● ● ● ● ● ● ● ●
Factor=3:  ●     ●     ●     ●
```

- **Pro:** Extremely fast — just array slicing
- **Con:** No spatial awareness; dense clusters stay dense

### Voxel Grid
Divide 3D space into a regular grid of cubes (voxels). For each occupied cell, keep the point **closest to the cell's centroid**.

```
┌────┬────┬────┐
│  ● │●   │  ● │   ← one representative per cell
├────┼────┼────┤
│    │  ● │●   │
└────┴────┴────┘
```

- **Pro:** Spatially uniform output, preserves shape
- **Con:** Slower; voxel size requires tuning

---

## Usage

```python
from sub_sampling_stratigies import sub_sample_pcd_decimation, sub_sample_pcd_voxel_grid

# Decimation — keep every 10th point
dec = sub_sample_pcd_decimation(factor=10, points_path="your_file.las")
dec.conv_to_o3d()

# Voxel grid — one point per 6-unit cell
vox = sub_sample_pcd_voxel_grid(voxel_size=6, points_path="your_file.las")
points = vox.store_voxels()
```

---

## Requirements

```
laspy
open3d
numpy
matplotlib
```

Install with:

```bash
pip install laspy open3d numpy matplotlib
```

---

## When to use which?

| | Decimation | Voxel Grid |
|---|---|---|
| Speed | Fast | Moderate |
| Spatial uniformity | Low | High |
| Preserves shape | Partially | Better |
| Tuning | `factor` | `voxel_size` |

Use **decimation** for a quick preview. Use **voxel grid** when spatial distribution matters.

## Gifs
![Decimation](decimation.gif)
![Voxel Grid](voxel_grid.gif)