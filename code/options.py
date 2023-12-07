import numpy as np
import argparse

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default="./code/model/shape_predictor_81_face_landmarks.dat")
    parser.add_argument('--init_hr', type=int, default=60)
    parser.add_argument('--hr_freq_range', type=list, default=[0.8, 2.5])
    parser.add_argument('--beta', type=float, default=0.95)
    parser.add_argument('--queue_size', type=int, default=256)
    parser.add_argument('--window_size', type=int, default=64)
    parser.add_argument('--queue_rawframe_size', type=int, default=3)
    kwargs = parser.parse_args()
    return kwargs

if __name__ == "__main__": 
    kwargs = get_options()
    print(kwargs)
