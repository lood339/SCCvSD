import random
from PIL import Image

import torch
from torch.utils.data.dataset import Dataset

class CameraDataset(Dataset):
    def __init__(self,
                 pivot_data,
                 positive_data,
                 batch_size,
                 num_batch,
                 data_transform):
        """
        :param pivot_data: N x 1 x H x W
        :param positive_data: N x 1 x H x W
        :param batch_size:
        :param num_batch:
        """
        super(CameraDataset, self).__init__()
        assert pivot_data.shape == positive_data.shape

        self.pivot_data = pivot_data
        self.positive_data = positive_data
        self.batch_size = batch_size
        self.num_batch = num_batch
        self.data_transform = data_transform
        self.num_camera = pivot_data.shape[0]

        self.positive_index = []
        self.negative_index = []

        self._sample_once()

    def _sample_once(self):
        batch_size = self.batch_size
        num_batch = self.num_batch

        self.positive_index = []
        self.negative_index = []
        num = batch_size * num_batch
        c_set = set([i for i in range(self.num_camera)])
        for i in range(num):
            idx1, idx2 = random.sample(c_set, 2)  # select two indices in random
            self.positive_index.append(idx1)
            self.negative_index.append(idx2)

        assert len(self.positive_index) == num
        assert len(self.negative_index) == num

    def __getitem__(self, index):
        """
        :param index:
        :return:
        """
        assert index < self.num_batch

        n, c, h, w = self.pivot_data.shape
        batch_size = self.batch_size

        start_index = batch_size * index
        end_index = start_index + batch_size
        positive_index = self.positive_index[start_index:end_index]
        negative_index = self.negative_index[start_index:end_index]

        x1 = torch.zeros(batch_size * 2, c, h, w)
        x2 = torch.zeros(batch_size * 2, c, h, w)
        label = torch.zeros(batch_size * 2)

        for i in range(batch_size):
            idx1, idx2 = positive_index[i], negative_index[i]
            pivot = self.pivot_data[idx1].squeeze()
            pos = self.positive_data[idx1].squeeze()
            neg = self.pivot_data[idx2].squeeze()

            pivot = Image.fromarray(pivot)
            pos = Image.fromarray(pos)
            neg = Image.fromarray(neg)

            #print('{} {} '.format(pivot.shape, self.data_transform(pivot).shape))
            x1[i*2+0, :] = self.data_transform(pivot)
            x1[i*2+1, :] = self.data_transform(pivot)
            x2[i*2+0, :] = self.data_transform(pos)
            x2[i*2+1, :] = self.data_transform(neg)

            label[i*2+0] = 1
            label[i*2+1] = 0
        x1 = torch.tensor(x1, requires_grad=True)
        x2 = torch.tensor(x2, requires_grad=True)
        return x1, x2, label

    def __len__(self):
        return self.num_batch

def ut():
    import scipy.io as sio
    import numpy as np
    import torchvision.transforms as transforms
    data = sio.loadmat('../../data/train_data_10k.mat')
    pivot_images = data['pivot_images']
    positive_images = data['positive_images']

    normalize = transforms.Normalize(mean=[0.0188],
                                     std=[0.128])

    data_transform = transforms.Compose(
        [transforms.ToTensor(),
         normalize,
         ]
    )

    batch_size = 32
    num_batch = 64
    dataset = CameraDataset(pivot_images, positive_images, batch_size, num_batch, data_transform)

    for i in range(len(dataset)):
        x1, x2, label1 = dataset[i]
        print('{} {} {}'.format(x1.shape, x2.shape, label1.shape))
        break





if __name__ == '__main__':
    ut()

