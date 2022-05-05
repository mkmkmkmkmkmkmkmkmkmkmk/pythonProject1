# 标准前馈神经网络,进行图像分类，效果不好
# set the matplotlib backend so figures can be saved in the background
import matplotlib
from scipy.constants import lb

matplotlib.use("Agg")
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.python.keras import models, layers, metrics, initializers, optimizers
from api.imageCrawler.imageCrawler.model.simple_vggnet import SimpleVGGNet
# from imutils import paths
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import load_model
import numpy as np
# from tensorflow.keras.utils import to_categorical
# import argparse
import random
import pickle
import cv2
import os
import warnings
warnings.filterwarnings("ignore")


# 获取文件夹内所有文件
def getFileList(dir, Filelist, ext=None):
    """
    获取文件夹及其子文件夹中文件列表
    输入 dir：文件夹根目录
    输入 ext: 扩展名
    返回： 文件路径列表
    """
    newDir = dir
    if os.path.isfile(dir):
        if ext is None:
            Filelist.append(dir)
        else:
            if ext in dir[-3:]:
                Filelist.append(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileList(newDir, Filelist, ext)

    return Filelist


# 训练的方法
def train():
    # initialize the data and labels
    print("[INFO] loading images...")
    data = []
    labels = []

    imagePaths = []
    paths = 'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/electricity/hotwater/'
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(getFileList(paths, imagePaths)))
    random.seed(42)
    random.shuffle(imagePaths)

    # 浣熊
    for imagePath in imagePaths:
        # load the image, resize the image to be 64x64 pixels (ignoring
        # aspect ratio), flatten the image into 64x64x3=3072 pixel image
        # into a list, and store the image in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (64, 64))
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = 'hotwater'  # imagePath.split(os.path.sep)[-2]
        labels.append(label)

    imagePaths = []
    paths = 'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/electricity/refigerator/'
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(getFileList(paths, imagePaths)))
    random.seed(42)
    random.shuffle(imagePaths)

    # 鱼
    for imagePath in imagePaths:
        # load the image, resize the image to be 64X64 pixels (ignoring
        # aspect ratio), flatten the image into 64x64x3=3072 pixel image
        # into a list, and store the image in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (64, 64))
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = 'refigerator'  # imagePath.split(os.path.sep)[-2]
        labels.append(label)

    imagePaths = []
    paths = 'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/electricity/washer/'
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(getFileList(paths, imagePaths)))
    random.seed(42)
    random.shuffle(imagePaths)

    # 猫
    for imagePath in imagePaths:
        # load the image, resize the image to be 64x64 pixels (ignoring
        # aspect ratio), flatten the image into 64x64x3=3072 pixel image
        # into a list, and store the image in the data list
        image = cv2.imread(imagePath)
        # 正常CNN输入是224 x244x 3，这里进行缩小成64 x 64 x 3，为了提高计算速度
        image = cv2.resize(image, (64, 64))
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = 'washer'  # imagePath.split(os.path.sep)[-2]
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # partition the data into training and testing splits using 75% of
    # the data for training and the remaining 25% for testing
    # test_X,test_Y ia validation dataset
    (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)
    print(trainX.shape)
    # convert the labels from integers to vectors (for 2-class, binary
    # classification you should use Keras' to_categorical function
    # instead as the scikit-learn's LabelBinarizer will not return a
    # vector)
    # 转换标签 one_hot格式
    lb = LabelBinarizer()
    trainY = lb.fit_transform(trainY)
    testY = lb.transform(testY)

    # define the 3072-1024-512-3 architecture using Keras
    # 建立卷积神经网络CNN：定义网络模型结构3072-1024-512-3 像素点
    model = SimpleVGGNet.build(width=64, height=64, depth=3,
                               classes=len(lb.classes_))

    # Simple_VGGnet超参数
    INIT_LR = 0.01
    # 1个epoch相当于迭代了数据集中那么多数量（如3000)的图
    # 1个batch迭代100张图
    # 1个epotch:30batch
    EPOCHS = 80
    BS = 32

    print("[INFO] training network...")
    # 随机梯度下降法，支持动量参数，支持学习衰减率（每次更新后的学习率衰减值），支持Nesterov动量
    # keras. optimizers. SGD(1r=0.01,momentum=0.0，decay=0.0,nesterov=False )
    opt = optimizers.gradient_descent_v2.SGD(learning_rate=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])  # 损失函数:交叉熵

    # 网络模型训练
    # H = model.fit_generator(aug.flow(trainX, trainY, batch_size = BS),
    #                         validation_data= (testX, testY),
    #                         steps_per_epoch = len(trainX) // BS,
    #         epochs = EPOCHS)

    H = model.fit(x=trainX, y=trainY, validation_data=(testX, testY), epochs=EPOCHS, batch_size=32)
    return model, lb, testX, testY, EPOCHS, H


# 评估的方法,绘制训练损失和准确性
def evaluate(model, testX, testY, EPOCHS, H):
    # evaluate the network
    print("[INFO] evaluating network...")
    predictions = model.predict(x=testX, batch_size=32)  #
    print(classification_report(testY.argmax(axis=1),
                                predictions.argmax(axis=1), target_names=lb.classes_))
    # plot the training loss and accuracy
    N = np.arange(0, EPOCHS)
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(N, H.history["loss"], label="train_loss")
    plt.plot(N, H.history["val_loss"], label="val_loss")
    plt.plot(N, H.history["accuracy"], label="train_acc")
    plt.plot(N, H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy (Simple NN)")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.savefig(
        'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/simple_vggnet_plot.png')


# 保存模型
def savemodel(model, lb):
    # save the model and label binarizer to disk
    print("[INFO] serializing network and label binarizer...")
    model.save('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/simple_vggnet.h5',
               save_format="h5")
    f = open('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/simple_vggnet.pickle',
             "wb")
    f.write(pickle.dumps(lb))
    f.close()


# 测试模型
def testmodel():
    # load the input image and resize it to the target spatial dimensions
    image = cv2.imread('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/test_img/0.jpg')
    output = image.copy()
    image = cv2.resize(image, (64, 64))
    # scale the pixel values to [0, 1]
    image = image.astype("float") / 255.0
    # check to see if we should flatten the image and add a batch
    # dimension
    if 1 > 0:
        # image = image.flatten()
        # image = image.reshape((1, image.shape[0]))
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # otherwise, we must be working with a CNN -- don't flatten the
    # image, simply add the batch dimension
    else:
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    # load the model and label binarizer
    print("[INFO] loading network and label binarizer...")
    model = load_model(
        'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/simple_vggnet.h5')
    lb = pickle.loads(
        open('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/simple_vggnet.pickle',
             "rb").read())
    # make a prediction on the image
    preds = model.predict(image)
    # find the class label index with the largest corresponding
    # probability
    i = preds.argmax(axis=1)[0]
    label = lb.classes_[i]
    # array([[5.4622066e-01, 4.5377851e-01, 7.7963534e-07]], dtype=float32)
    # draw the class label + probability on the output image
    text = "{}: {:.2f}%".format(label, preds[0][i] * 100)
    cv2.putText(output, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 0, 255), 2)
    # show the output image
    cv2.imshow("Image", output)
    cv2.waitKey(0)


testmodel()

# model, lb, testX, testY, EPOCHS, H = train()
# evaluate(model, testX, testY, EPOCHS, H)
# savemodel(model, lb)
