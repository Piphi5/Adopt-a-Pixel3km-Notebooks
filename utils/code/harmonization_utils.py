harmonization_table = {
    "Trees": ["Trees", "CEO_Trees", "GO_Trees"],
    "Shrubland": ["Shrubland", "CEO_Shrubland", "GO_Shrub"],
    "Grassland": ["Grassland", "CEO_Grassland", "GO_Grass"],
    "Cropland": ["Cropland", "CEO_Cropland", "GO_Cultivated"],
    "Built-up": ["Built-up", "CEO_BuiltUp", "GO_BuiltUp"],
    "Barren": ["Barren / Sparse Vegetation", "CEO_Barren", "GO_Barren"],
    "Water": ["Open Water", "CEO_Water", "GO_Water"],
}

harmonization_table_lookup = {"World Cover": 0, "CEO": 1, "GLOBE": 2}

ceo_to_worldcover_lookup = {
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
