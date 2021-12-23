import os

import pandas as pd


def get_csvs(directory):
    df = pd.DataFrame()
    csvs = [file for file in os.listdir(directory) if file.endswith(".csv")]
    for csv in csvs:
        temp = pd.read_csv(f"{directory}/{csv}")
        df = df.append(temp)

    return df
