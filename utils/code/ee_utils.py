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

sentinel_image_viz_params = {
    "bands": ["B4_median", "B3_median", "B2_median"],
    "min": 0,
    "max": 0.3,
    "gamma": 1.4,
}

worldcover_visualization = {
    "bands": ["Map"],
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

def add_ee_layer(self, ee_object, vis_params, name):

    try:
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict["tile_fetcher"].url_format,
                attr="Google Earth Engine",
                name=name,
                overlay=True,
                control=True,
            ).add_to(self)
        # display ee.ImageCollection()
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict["tile_fetcher"].url_format,
                attr="Google Earth Engine",
                name=name,
                overlay=True,
                control=True,
            ).add_to(self)
        # display ee.Geometry()
        elif isinstance(ee_object, ee.geometry.Geometry):
            folium.GeoJson(
                data=ee_object.getInfo(), name=name, overlay=True, control=True
            ).add_to(self)
        # display ee.FeatureCollection()
        elif isinstance(ee_object, ee.featurecollection.FeatureCollection):
            ee_object_new = ee.Image().paint(ee_object, 0, 2)
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict["tile_fetcher"].url_format,
                attr="Google Earth Engine",
                name=name,
                overlay=True,
                control=True,
            ).add_to(self)

    except Exception as e:
        print("Could not display {}".format(name))
        print(str(e))

def sentinel_cloud_mask(image):
    qa = image.select("QA60")
    cloudBit = 1 << 10
    cirrusBit = 1 << 1

    mask = qa.bitwiseAnd(cloudBit) and (qa.bitwiseAnd(cirrusBit).eq(0))

    return image.updateMask(mask).divide(10000)
