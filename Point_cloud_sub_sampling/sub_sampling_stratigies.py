import laspy as lp
import numpy as np
import open3d as o3d

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


class sub_sample_pcd_decimation:
    def __init__(self , factor , points_path):
        self.las = lp.read(points_path)
        self.factor = factor
        self.points = np.vstack([self.las.x, self.las.y, self.las.z]).T
    
    def conv_to_o3d(self):
        decimated_points = self.points[::self.factor]
        # len(decimated_points)

        pcd_las_o3d = o3d.geometry.PointCloud()
        pcd_las_o3d.points = o3d.utility.Vector3dVector(decimated_points)
        o3d.visualization.draw_geometries([pcd_las_o3d])

class sub_sample_pcd_voxel_grid:
    def __init__(self, voxel_size , points_path):
        self.voxel_size= voxel_size
        self.las = lp.read(points_path)
        self.points = np.vstack([self.las.x, self.las.y, self.las.z]).T

    def _calc_voxel_number(self):
        non_empty_voxel_keys, inverse, nb_pts_per_voxel= np.unique(((self.points - np.min(self.points, axis=0)) // self.voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
        idx_pts_vox_sorted = np.argsort(inverse)
        len(non_empty_voxel_keys)
        return non_empty_voxel_keys, nb_pts_per_voxel , idx_pts_vox_sorted
    

    def store_voxels(self):
                
        voxel_grid={}
        grid_barycenter,grid_candidate_center=[],[]
        last_seen=0
        non_empty_voxel_keys, nb_pts_per_voxel ,idx_pts_vox_sorted = self._calc_voxel_number()

        for idx,vox in enumerate(non_empty_voxel_keys):
            voxel_grid[tuple(vox)]=self.points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
            grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
            grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)]-np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
            last_seen+=nb_pts_per_voxel[idx]

        return  grid_candidate_center

def main():
    las_path = r"./Data/madison.las"   # fix extension
    # -------------------------
    # Decimation Subsampling
    # -------------------------
    decimation = sub_sample_pcd_decimation(
        factor=10,
        points_path=las_path
    )

    decimation.conv_to_o3d()

    print("Decimation done")


    # -------------------------
    # Voxel Grid Subsampling
    # -------------------------
    voxel = sub_sample_pcd_voxel_grid(
        voxel_size=6,
        points_path=las_path
    )

    voxel_points = voxel.store_voxels()
    pcd_voxel = o3d.geometry.PointCloud()
    pcd_voxel.points = o3d.utility.Vector3dVector(voxel_points)
    print("Voxel subsampling done")
    # -------------------------
    # Visualization
    # -------------------------
    o3d.visualization.draw_geometries(
        [pcd_voxel],
        window_name="Voxel Grid Subsample"
    )


if __name__ == "__main__":
    main()