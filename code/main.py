import numpy as np
import cv2

import rppg_dataset
import core
import options
kwargs = options.get_options()

if __name__ == "__main__":
    print(kwargs)
    data = rppg_dataset.DataReader('data', [])
    result = core.process_data(data)
    print("Hello world!")
    frames = data.read()
    for frame in frames[0]:
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
