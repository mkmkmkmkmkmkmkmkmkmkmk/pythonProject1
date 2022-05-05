# 标准前馈神经网络,进行图像分类，效果不好
# set the matplotlib backend so figures can be saved in the background
import matplotlib
from scipy.constants import lb

matplotlib.use("Agg")
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
# from keras import models, layers, metrics, initializers
# from imutils import paths
from tensorflow.python.keras.optimizers import adam_v2
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import load_model
import numpy as np
# import argparse
import random
import pickle
import cv2
import os


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
    paths = 'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/electricity/raccoon/hotwater/'
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(getFileList(paths, imagePaths)))
    random.seed(42)
    random.shuffle(imagePaths)

    # 热水器
    for imagePath in imagePaths:
        # load the image, resize the image to be 32x32 pixels (ignoring
        # aspect ratio), flatten the image into 32x32x3=3072 pixel image
        # into a list, and store the image in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (32, 32)).flatten()
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = 'hotwater'  # imagePath.split(os.path.sep)[-2]
        labels.append(label)

    imagePaths = []
    paths = 'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/electricity/conditioner/'
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(getFileList(paths, imagePaths)))
    random.seed(42)
    random.shuffle(imagePaths)

    # 空调
    for imagePath in imagePaths:
        # load the image, resize the image to be 32x32 pixels (ignoring
        # aspect ratio), flatten the image into 32x32x3=3072 pixel image
        # into a list, and store the image in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (32, 32)).flatten()
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = 'conditioner'  # imagePath.split(os.path.sep)[-2]
        labels.append(label)

    imagePaths = []
    paths = 'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/electricity/washer/'
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(getFileList(paths, imagePaths)))
    random.seed(42)
    random.shuffle(imagePaths)

    # 洗衣机
    for imagePath in imagePaths:
        # load the image, resize the image to be 32x32 pixels (ignoring
        # aspect ratio), flatten the image into 32x32x3=3072 pixel image
        # into a list, and store the image in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (32, 32)).flatten()
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

    # convert the labels from integers to vectors (for 2-class, binary
    # classification you should use Keras' to_categorical function
    # instead as the scikit-learn's LabelBinarizer will not return a
    # vector)
    # 转换标签 one_hot格式
    lb = LabelBinarizer()
    trainY = lb.fit_transform(trainY)
    testY = lb.transform(testY)

    # define the 3072-1024-512-3 architecture using Keras
    # 定义网络模型结构3072-1024-512-3 像素点
    model = Sequential()
    model.add(Dense(1024, input_shape=(3072,), activation="sigmoid"))
    model.add(Dense(512, activation="sigmoid"))
    model.add(Dense(len(lb.classes_), activation="softmax"))

    # initialize our initial learning rate and # of epochs to train for
    INIT_LR = 0.01
    # 1个epoch相当于迭代了3000多张图
    # 1个batch迭代100张图
    # 1个epotch:30batch
    EPOCHS = 80
    # compile the model1 using Adam as our optimizer and categorical
    # cross-entropy loss (you'll want to use binary_crossentropy
    # for 2-class classification)
    print("[INFO] training network...")
    opt = adam_v2.Adam(learning_rate=INIT_LR)
    model.compile(loss="sparse_categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

    # 网络模型训练
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
    plt.savefig('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity'
                '/simple_nn_plot.png')


# 保存模型
def savemodel(model, lb):
    # save the model1 and label binarizer to disk
    print("[INFO] serializing network and label binarizer...")
    model.save('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity'
               '/simple_nn_lb.h5',
               save_format="h5")
    f = open('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity'
             '/simple_nn_lb.pickle',
             "wb")
    f.write(pickle.dumps(lb))
    f.close()


# 测试模型
def testmodel():
    # load the input image and resize it to the target spatial dimensions
    image = cv2.imread('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/test_img/0.jpg')
    output = image.copy()
    image = cv2.resize(image, (32, 32))
    # scale the pixel values to [0, 1]
    image = image.astype("float") / 255.0
    # check to see if we should flatten the image and add a batch
    # dimension
    image = image.flatten()
    image = image.reshape((1, image.shape[0]))
    # otherwise, we must be working with a CNN -- don't flatten the
    # image, simply add the batch dimension


    # load the model1 and label binarizer
    print("[INFO] loading network and label binarizer...")
    model = load_model(
        'C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/simple_nn_lb.h5')
    lb = pickle.loads(
        open('C:/Users/DELL/PycharmProjects/pythonProject1/api/imageCrawler/imageCrawler/data/res_electricity/simple_nn_lb.pickle',
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


# testmodel()

model1, lb, testX, testY, EPOCHS, H = train()
evaluate(model1, testX, testY, EPOCHS, H)
savemodel(model1, lb)
