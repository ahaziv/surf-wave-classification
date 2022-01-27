import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import SurfwavesDataset


def to_cuda(x):
    if use_gpu:
        x = x.to('cuda')
    return x


class SurfCovNet(nn.Module):
    def __init__(self, inp_size, num_class):
        super(SurfCovNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(inp_size, 16, kernel_size=5, stride=1, padding=3, dilation=1, bias=False),
            nn.ReLU(),
            nn.MaxPool2d(1),
            nn.BatchNorm2d(16))                     # for batchnorm bias isn't necessary
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 16, kernel_size=5, stride=1, padding=2, dilation=1, bias=False),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.BatchNorm2d(16))                     # for batchnorm bias isn't necessary
        self.layer3 = nn.Sequential(
            nn.Conv2d(16, 20, kernel_size=5, stride=1, padding=2, dilation=1, bias=False),
            nn.ReLU(),
            nn.MaxPool2d(1),
            nn.BatchNorm2d(20))                     # for batchnorm bias isn't necessary
        self.layer4 = nn.Sequential(
            nn.Conv2d(20, 20, kernel_size=5, stride=1, padding=2, dilation=1, bias=False),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.BatchNorm2d(20))                     # for batchnorm bias isn't necessary
        self.layer5 = nn.Sequential(
            nn.Conv2d(20, 32, kernel_size=3, stride=1, padding=1, dilation=1, bias=False),
            nn.ReLU(),
            nn.MaxPool2d(1),
            nn.BatchNorm2d(32))                     # for batchnorm bias isn't necessary
        self.fc1 = nn.Sequential(
            nn.Linear(8*8*32, 100),
            nn.ELU())
            # nn.Dropout(p),
            # nn.BatchNorm1d(50)
        self.fc2 = nn.Sequential(
            nn.Linear(100, num_class),
            nn.ELU())
        self.dropout = nn.Dropout(p=0.5)
        self.logsoftmax = nn.LogSoftmax()

    def forward(self, x):
        out = self.layer1(x)
        # out = self.dropout(out)
        out = self.layer2(out)
        # out = self.dropout(out)
        out = self.layer3(out)
        # out = self.dropout(out)
        out = self.layer4(out)
        out = self.dropout(out)
        out = self.layer5(out)
        out = out.view(out.size(0), -1)
        out = self.fc1(out)
        out = self.fc2(out)

        return self.logsoftmax(out)


# ---------------------------------------------------------- main ---------------------------------------------------- #
if __name__ == '__main__':
    use_gpu = torch.cuda.is_available()
    print(use_gpu)

    # HyperParameters
    batch_size = 64
    input_size = 3072
    num_classes = 10
    num_epochs = 100
    learning_rate = 0.001

    # obtaining normalization values from the dataset


    # transforms and normalization
    transform_train = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((mean_dst[0], norm_dst[1], norm_dst[2],),
                             (std_dst[0], std_dst[1], std_dst[2])),
    ])
    transform_test = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465,),
                             (0.2470, 0.2434, 0.2615)),
    ])

    # loading data
    train_dataset = dsets.CIFAR10(root='./data', train=True, transform=transforms.ToTensor(), download=True)
    test_dataset = dsets.CIFAR10(root='./data', train=False, transform=transforms.ToTensor(), download=True)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    cnn = SurfCovNet(input_size, num_classes)
    print('number of parameters: ', sum(param.numel() for param in cnn.parameters()))
    cnn = to_cuda(cnn)

    criterion = nn.NLLLoss()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        learning_rate = 0.1 * np.exp(-6.9 * epoch)
        for i, (images, labels) in enumerate(train_loader):
            images = to_cuda(images)
            labels = to_cuda(labels)

            # forward
            outputs = cnn(images)
            loss = criterion(outputs, labels)

            # backward
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm(cnn.parameters(), max_norm=1)

            # optimize
            optimizer.step()

            if (i+1) % 100 == 0:
                print('Epoch [%d/%d], Iter [%d/%d] Loss: %.4f'
                    % (epoch + 1, num_epochs, i + 1, len(train_dataset) // batch_size, loss.item()))

        if (epoch+1) % 10 == 0:
            cnn.eval()
            correct = 0
            total = 0
            for images, labels in test_loader:
                images = to_cuda(images)
                outputs = cnn(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted.cpu() == labels).sum()

                print('Test Accuracy of the model     images = to_cuda(images)on the 10000 test images: %d %%' % (100 * correct/total))
    torch.save(cnn.state_direct(), 'cnn.pkl')