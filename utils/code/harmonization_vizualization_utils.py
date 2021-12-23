import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

harmonization_table = {
    "Trees": ["Trees", "CEO_Trees", "GO_Trees"],
    "Shrubland": ["Shrubland", "CEO_Shrubland", "GO_Shrub"],
    "Grassland": ["Grassland", "CEO_Grassland", "GO_Grass"],
    "Cropland": ["Cropland", "CEO_Cropland", "GO_Cultivated"],
    "Built-up": ["Built-up", "CEO_BuiltUp", "GO_BuiltUp"],
    "Barren": ["Barren / Sparse Vegetation", "CEO_Barren", "GO_Barren"],
    "Water": ["Open Water", "CEO_Water", "GO_Water"],
}

dataset_value_map = {"World Cover": 0, "CEO": 1, "GLOBE": 2}

go_legend = {
    "GO_Grass": "#00F100",
    "GO_Barren": "#AA7941",
    "GO_Trees": "#007500",
    "GO_Shrub": "#DBED00",
    "GO_Cultivated": "#FF00D6",
    "GO_Water": "#00B7F2",
    "GO_BuiltUp": "#FF8080",
}

ceo_legend = {
    "Trees_CanopyCover": "#007500",
    "bush/scrub": "#DBED00",
    "grass": "#00F100",
    "cultivated vegetation": "#FF00D6",
    "Water>treated pool": "#00F1DE",
    "Water>lake/ponded/container": "#00B7F2",
    "Water>rivers/stream": "#1527F6",
    "Water>irrigation ditch": "#007570",
    "shadow": "#000000",
    "unknown": "#C8D2D3",
    "Bare Ground": "#AA7941",
    "Building": "#FF8080",
    "Impervious Surface (no building)": "#FF0000",
}

harmonized_ceo = {
    "CEO_Trees": "#007500",
    "CEO_Shrubland": "#DBED00",
    "CEO_Grassland": "#00F100",
    "CEO_Cropland": "#FF00D6",
    "CEO_BuiltUp": "#FF8080",
    "CEO_Barren": "#AA7941",
    "CEO_Water": "#00B7F2",
}

worldcover_legend = {
    "Trees": "#006400",
    "Shrubland": "#ffbb22",
    "Grassland": "#ffff4c",
    "Cropland": "#f096ff",
    "Built-up": "#fa0000",
    "Barren / Sparse Vegetation": "#b4b4b4",
    "Open Water": "#0064c8",
    "Herbaceous Wetland": "#0096a0",
    "Moss and Lichen": "#fae6a0",
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

ceo_to_wc_lookup = {
    "Trees_CanopyCover": "Trees",
    "bush/scrub": "Shrubland",
    "grass": "Grassland",
    "cultivated vegetation": "Cropland",
    "Water>lake/ponded/container": "Open Water",
    "Water>rivers/stream": "Open Water",
    "Water>irrigation ditch": "Open Water",
    "Water>treated pool": "Open Water",
    "Bare Ground": "Barren / Sparse Vegetation",
    "Building": "Built-up",
    "Impervious Surface (no building)": "Built-up",
}


def sentinel_cloud_mask(image):
    qa = image.select("QA60")
    cloudBit = 1 << 10
    cirrusBit = 1 << 1

    mask = qa.bitwiseAnd(cloudBit) and (qa.bitwiseAnd(cirrusBit).eq(0))

    return image.updateMask(mask).divide(10000)


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


def ceo_harmonization(df):
    df["CEO_BuiltUp"] = (
        df["Land Cover Elements:Building"]
        + df["Land Cover Elements:Impervious Surface (no building)"]
    )
    df["CEO_Trees"] = df["Land Cover Elements:Trees_CanopyCover"]
    df["CEO_Shrubland"] = df["Land Cover Elements:bush/scrub"]
    df["CEO_Grassland"] = df["Land Cover Elements:grass"]
    df["CEO_Cropland"] = df["Land Cover Elements:cultivated vegetation"]
    df["CEO_Water"] = (
        df["Land Cover Elements:Water>treated pool"]
        + df["Land Cover Elements:Water>rivers/stream"]
        + df["Land Cover Elements:Water>irrigation ditch"]
        + df["Land Cover Elements:Water>lake/ponded/container"]
    )
    df["CEO_Barren"] = df["Land Cover Elements:Bare Ground"]


def aoi_plot(df, name, classifications, colors, directory=""):
    title = f"Mean Composition -- {name}"
    filename = f"{title}.png"
    if directory:
        filename = f"{directory}/{filename}"

    plt.figure()
    mean = np.mean(df[classifications])
    patches, text, _ = plt.pie(mean, colors=colors, autopct="%.2f", pctdistance=1.1)
    plt.legend(patches, classifications, bbox_to_anchor=(1.15, 1), loc="upper left")
    plt.title(title, fontweight="bold")
    plt.savefig(filename)
    plt.show()


def bar_comparison_plot(df, datasets, directory=""):
    title = ""
    for dataset in datasets[:-1]:
        title += f"{dataset} vs. "
    title += datasets[-1]
    title = f"{title} Landcover Class Distributions"

    column_list = [dataset_value_map[dataset] for dataset in datasets]

    color = sns.color_palette()
    sns.set_style("darkgrid")
    fig, axs = plt.subplots(len(harmonization_table.keys()), 1)
    fig.set_figwidth(10)
    fig.set_figheight(15)
    fig.suptitle(title, fontweight="bold", fontsize=18)

    fig.tight_layout(pad=3.0)
    fig.subplots_adjust(top=0.94)
    for i, item in enumerate(harmonization_table.items()):
        classification, total_columns = item
        desired_columns = [total_columns[num] for num in column_list]
        axs[i].bar(datasets, np.mean(df[desired_columns]), color=color)
        axs[i].set_title(f"Mean {classification} Distribution")
        axs[i].title.set_weight("bold")
    if directory:
        plt.savefig(f"{directory}/{title} Bar Graph.png")
    else:
        plt.savefig(f"{title} Bar Graph.png")
    plt.show()
