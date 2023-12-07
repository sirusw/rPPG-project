import numpy as np
import argparse

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default="./code/model/shape_predictor_81_face_landmarks.dat")
    parser.add_argument('--bvp_range', type=str, default="./code/video/1.mp4")
    kwargs = parser.parse_args()
    return kwargs

if __name__ == "__main__": 
    kwargs = get_options()
    print(kwargs)
