import numpy as np

import rppg_dataset
import utils
import options
kwargs = options.get_options()

def process_data(raw_data: rppg_dataset.DataReader) -> np.array: 
    return np.array([raw_data])

if __name__ == "__main__":
    data = rppg_dataset.DataReader()
    result = process_data(data)
    utils.plot_data(result, "Title", "X", "Y")
    