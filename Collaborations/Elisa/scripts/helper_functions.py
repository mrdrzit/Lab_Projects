import numpy as np
import pandas as pd

def find_sections(dataframe, framerate):
    in_interval = False
    start_idx = None
    intervals = pd.DataFrame(columns=["start", "end", "duration"])
    for idx, row in dataframe.iterrows():
        value = row[0]
        if value == 1 and not in_interval:
            start_idx = idx
            in_interval = True
        elif value == 0 and in_interval:
            duration = (idx - (start_idx - 1)) * (1 / framerate)
            new_dataframe = pd.DataFrame(data=[[start_idx, idx, duration]], columns=["start", "end", "duration"])
            intervals = pd.concat([intervals, new_dataframe])
            in_interval = False

    if in_interval:
        duration = (idx - (start_idx - 1)) * (1 / framerate)
        intervals = pd.concat([intervals, pd.DataFrame({"start": [start_idx], "end": [idx], "duration": [duration]})], ignore_index=True)
    return intervals


def cumulative_distribution(array):
    """
    Calculate the cumulative distribution function of an array of values.
    
    """
    values, counts = np.unique(array, return_counts=True)
    probabilities = counts / counts.sum()
    cdf = np.cumsum(probabilities)
    return values, cdf

def cdf(sample, x, sort = False):
    # Sorts the sample, if unsorted
    if sort:
        sample.sort()
    # Counts how many observations are below x
    cdf = sum(sample <= x)
    # Divides by the total number of observations
    cdf = cdf / len(sample)
    return cdf
