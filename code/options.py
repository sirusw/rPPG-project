import numpy as np
import argparse

def get_options():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--path', type=str, default='./data/')
    parser.add_argument('--mode', type=str, default='train')
    parser.add_argument('--save', action='store_true')
    parser.add_argument('--save_path', type=str, default='./save/') 
                        
    kwargs = parser.parse_args()
    return kwargs

if __name__ == "__main__": 
    kwargs = get_options()
    print(kwargs)
