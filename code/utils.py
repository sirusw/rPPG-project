import base64
import os
import matplotlib.pyplot as plt
import numpy as np
import options
kwargs = options.get_options()

def plot_data(x, y, title, xlabel, ylabel):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def save(data, file: str):
    if not os.path.exists(kwargs["save_path"]):
        os.mkdir(kwargs["save_path"])
    file_path = kwargs["save_path"] + file
    np.save(file_path, data)
    return file_path

if __name__ == "__main__":
    text = b'binary\x00string'
    output = base64.b64encode(text)
    print(output)
