from torch.utils.data import Dataset
import pandas as pd
import torch
import cv2
import os
import numpy as np


class SurfwavesDataset(Dataset):
    def __init__(self, csv_file, directory, label_type='swell', transform=None):
        self.root_dir = directory
        self.annotations = pd.read_csv(csv_file, encoding="ISO-8859-1")
        self.transform = transform
        self.label_type = label_type

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        index += 1
        im_path = os.path.join(self.root_dir, self.annotations.iloc[index, 0][:-1])
        image = cv2.imread(im_path, cv2.COLOR_BGR2RGB)
        y_label = {
            'swell': torch.tensor(self.swell_labels(self.annotations.iloc[index, 5])),
            'rating': torch.tensor(int(self.annotations.iloc[index, 3] + self.annotations.iloc[index, 4]))
        }.get(self.label_type, torch.tensor(self.swell_labels(self.annotations.iloc[index, 5])))

        if self.transform:
            image = self.transform(image=image)['image']
        return [image, y_label]

    @staticmethod
    def swell_labels(string: str):
        '''
        this function translates a swell height string such as '0.1-0.6m' to a labeled integer between 0 and 5

        '''
        if string == 'Flat\n':
            return 0
        swell = string[:-2]
        swell = swell.split('-')
        mean_swell = np.mean([float(i) for i in swell])
        if mean_swell < 0.4:
            return 0
        elif mean_swell < 0.7:
            return 1
        elif mean_swell < 1.1:
            return 2
        elif mean_swell < 2.:
            return 3
        elif mean_swell < 4.:
            return 4
        else:
            return 5


class LeafData(Dataset):
    def __init__(self, data, directory, transform=None):
        self.data = data
        self.directory = directory
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # import
        path = os.path.join(self.directory, self.data.iloc[idx]['image_id'])
        image = cv2.imread(path, cv2.COLOR_BGR2RGB)

        # augmentations
        if self.transform is not None:
            image = self.transform(image=image)['image']

        return image

