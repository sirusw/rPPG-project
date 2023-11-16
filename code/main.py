import numpy as np

import rppg_dataset
import core
import options
kwargs = options.get_options()

if __name__ == "__main__":
    print(kwargs)
    data = rppg_dataset.DataReader()
    result = core.process_data(data)
    print("Hello world!")
