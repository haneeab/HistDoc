
import torch
import torch.nn as nn

def dil_block(in_c, out_c):
    conv = nn.Sequential(
        nn.Conv2d(in_c, out_c, kernel_size=3, stride=1, padding=1, dilation=1),
        nn.BatchNorm2d(out_c),
        nn.ReLU(inplace=True),

        nn.Conv2d(out_c, out_c, kernel_size=3, stride=1, padding=1, dilation=1),
        nn.BatchNorm2d(out_c),
        nn.ReLU(inplace=True),

        nn.Conv2d(out_c, out_c, kernel_size=3, stride=1, padding=2, dilation=2),
        nn.BatchNorm2d(out_c),
        nn.ReLU(inplace=True),

        nn.Conv2d(out_c, out_c, kernel_size=3, stride=1, padding=2, dilation=2),
        nn.BatchNorm2d(out_c),
        nn.ReLU(inplace=True),


        )
    return conv

def encoding_block(in_c, out_c):
    conv = nn.Sequential(
        nn.Conv2d(in_c, out_c, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(out_c),
        nn.ReLU(inplace=True),

        )
    return conv

def encoding_block1(in_c, out_c):
    conv = nn.Sequential(
        nn.Conv2d(in_c, out_c, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(out_c),
        nn.ReLU(inplace=True),

        nn.Conv2d(out_c, out_c, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(out_c),
        nn.ReLU(inplace=True),

        )
    return conv

class unet_model(nn.Module):
    def __init__(self,out_channels=1,features=[16, 32]):
        super(unet_model,self).__init__()


        self.dil1 = dil_block(3,features[0])

        self.pool1 = nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))

        self.dil2 = dil_block(features[0],features[0])

        self.pool2 = nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))

        self.dil3 = dil_block(features[0],features[0])

        self.pool3 = nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))

        self.dil4 = dil_block(features[0],features[0])

        self.pool4 = nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))

        self.bott = encoding_block1(features[0],features[0])

        self.tconv1 = nn.ConvTranspose2d(features[0], features[0], kernel_size=2, stride=2)

        self.conv1 = encoding_block(features[1],features[0])

        self.tconv2 = nn.ConvTranspose2d(features[0], features[0], kernel_size=2, stride=2)

        self.conv2 = encoding_block(features[1],features[0])

        self.tconv3 = nn.ConvTranspose2d(features[0], features[0], kernel_size=2, stride=2)

        self.conv3 = encoding_block(features[1],features[0])

        self.tconv4 = nn.ConvTranspose2d(features[0], features[0], kernel_size=2, stride=2)

        self.conv4 = encoding_block1(features[1],features[0])

        self.final_layer = nn.Conv2d(features[0],out_channels, kernel_size=1)

    def forward(self,x):
        dil_1 = self.dil1(x)

        pool_1 = self.pool1(dil_1)

        dil_2 = self.dil2(pool_1)

        pool_2 = self.pool2(dil_2)

        dil_3 = self.dil3(pool_2)

        pool_3 = self.pool3(dil_3)

        dil_4 = self.dil4(pool_3)

        pool_4 = self.pool4(dil_4)

        bott = self.bott(pool_4)

        tconv_1 = self.tconv1(bott)

        concat1 = torch.cat((tconv_1, dil_4), dim=1)

        conv_1 = self.conv1(concat1)

        tconv_2 = self.tconv2(conv_1)

        concat2 = torch.cat((tconv_2, dil_3), dim=1)

        conv_2 = self.conv2(concat2)

        tconv_3 = self.tconv3(conv_2)

        concat3 = torch.cat((tconv_3, dil_2), dim=1)

        conv_3 = self.conv3(concat3)

        tconv_4 = self.tconv4(conv_3)

        concat4 = torch.cat((tconv_4, dil_1), dim=1)

        conv_4 = self.conv4(concat4)

        x = self.final_layer(conv_4)

        return x


import glob
import os
from dataset import Pinkas_Binary
if __name__ == '__main__':
    from torch.utils.data import Dataset, DataLoader
    folderPaths = '../Datasets/pinkas_BinaryAnalysisLayout'
    #### Train Datasets
    x_train_dir = glob.glob(os.path.join(folderPaths, 'train', 'imgs', '*.*'))
    x_train_dir.sort()

    y_train_dir = glob.glob(os.path.join(folderPaths,'train','masks','*.*'))
    y_train_dir.sort()
    print("Train set size ", len(x_train_dir))
    print(x_train_dir)

    xisGray = False,
    patchSize = 512
    datasets = Pinkas_Binary(x_train_dir, y_train_dir, patchSize=512, isGray=False)
    datasetPinkas = DataLoader(datasets)
    k = 0
    #model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # initilize the model
    model = unet_model(out_channels=2).to(device)
    for idx, data in enumerate(datasetPinkas):
        imgCropped, maskCropped = data[0],data[1]
        if k == 10:
            break;
        k = k + 1
        print(imgCropped.shape)
        print(model(imgCropped).shape)
        print(maskCropped.shape)
        exit(0)
