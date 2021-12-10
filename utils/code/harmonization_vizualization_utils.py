import seaborn as sns
import matplotlib.pyplot as plt

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


def aoi_plot(df, name, classifications, colors):
    plt.figure()
    mean = np.mean(df[classifications])
    patches, text, _ = plt.pie(mean, colors=colors, autopct="%.2f", pctdistance=1.1)
    plt.legend(patches, classifications, bbox_to_anchor=(1.15, 1), loc="upper left")
    plt.title(f"Mean Composition -- {name}", fontweight="bold")
    plt.show()


def bar_comparison_plot(df, datasets):
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

    plt.savefig(f"{title} Bar Graph.png")
    plt.show()
