from collections import Counter

import ee
import numpy as np

wc_id_classification_map = {
    10: "Trees",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Barren / Sparse Vegetation",
    70: "Snow and Ice",
    80: "Open Water",
    90: "Herbaceous Wetland",
    95: "Mangroves",
    100: "Moss and Lichen",
}


def wc_to_str(value):
    return wc_id_classification_map[value]


worldcover_converter = np.vectorize(wc_to_str)


def download_data(ee_image, features, index, folder, prefix):
    world_cover_points = ee.FeatureCollection(features)
    enriched = ee_image.reduceRegions(
        **{
            "collection": world_cover_points,
            "reducer": ee.Reducer.median(),
            "scale": 10,
        }
    )
    task = ee.batch.Export.table.toDrive(
        enriched, f"{prefix}-{index}", **{"folder": folder, "fileFormat": "CSV"}
    )

    task.start()
    return task


def download_ee_points(ee_image, ceo_features, increment, folder, prefix):
    tasks = [
        download_data(
            ee_image, ceo_features[i : i + increment], request_num, folder, prefix
        )
        for request_num, i in enumerate(range(0, len(ceo_features), increment))
    ]
    return tasks


def print_job_statuses(task_list, verbose=False):

    status_list = [task.status()["state"] for task in task_list]
    print(dict(Counter(status_list)))

    if verbose:
        print("All Task Information:")
        for num, task in enumerate(task_list):
            status = task.status()

            print(f"-------------{num}-------------")
            print(status)
