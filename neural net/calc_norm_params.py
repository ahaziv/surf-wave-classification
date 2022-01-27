import numpy as np
import pandas as pd
import torch
import torchvision
from torch.utils.data import Dataset, DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from SurfwavesDataset import SurfwavesDataset

if __name__ == '__main__':
    # PARAMS
    device = torch.device('cpu')
    num_workers = 4
    image_size = [256, 128]
    batch_size = 8
    data_path = os.path.join(os.path.dirname(os.getcwd()), 'data\\images')

    df = pd.read_csv(os.path.join(data_path, 'labels.csv'), encoding="ISO-8859-1")
    df.head()

    augs = A.Compose([A.Resize(height=image_size[1], width=image_size[0]), A.Normalize(mean=(0, 0, 0), std=(1, 1, 1)), ToTensorV2()])

    # dataset
    img_dataset = SurfwavesDataset(csv_file=os.path.join(data_path, 'labels.csv'), directory=data_path, transform=augs)

    # data loader
    image_loader = DataLoader(img_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)

    # display images
    for batch_idx, inputs in enumerate(image_loader):
        fig = plt.figure(figsize=(14, 7))
        for i in range(batch_size):
            ax = fig.add_subplot(2, 4, i + 1, xticks=[], yticks=[])
            plt.imshow(inputs[i].numpy().transpose(1, 2, 0))
        break

    # placeholders
    psum = torch.tensor([0.0, 0.0, 0.0])
    psum_sq = torch.tensor([0.0, 0.0, 0.0])

    # loop through images
    for inputs in tqdm(image_loader):
        psum += inputs.sum(axis=[0, 2, 3])
        psum_sq += (inputs ** 2).sum(axis=[0, 2, 3])

    # pixel count
    count = len(df) * image_size * image_size

    # mean and std
    total_mean = psum / count
    total_var = (psum_sq / count) - (total_mean ** 2)
    total_std = torch.sqrt(total_var)

    # output
    print('mean: ' + str(total_mean))
    print('std:  ' + str(total_std))
