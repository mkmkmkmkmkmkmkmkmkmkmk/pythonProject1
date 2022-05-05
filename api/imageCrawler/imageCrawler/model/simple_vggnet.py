# from keras import models, layers, metrics, initializers, optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
# from keras.layers import BatchNormalization
from tensorflow.python.keras.layers.core import Activation


"""
SimpleVGGNet属于用于目标检测的CNN。
"""


class SimpleVGGNet:
    # def softmax(x):
    #     """
    #     Compute the softmax function for each row of the input x.
    #     Arguments:
    #     x -- A N dimensional vector or M x N dimensional numpy matrix.
    #     Return:
    #     x -- You are allowed to modify x in-place
    #     """
    #     orig_shape = x.shape
    #
    #     if len(x.shape) > 1:
    #         # Matrix
    #         exp_minmax = lambda x: np.exp(x - np.max(x))
    #         denom = lambda x: 1.0 / np.sum(x)
    #         x = np.apply_along_axis(exp_minmax, 1, x)
    #         denominator = np.apply_along_axis(denom, 1, x)
    #
    #         if len(denominator.shape) == 1:
    #             denominator = denominator.reshape((denominator.shape[0], 1))
    #
    #         x = x * denominator
    #     else:
    #         # Vector
    #         x_max = np.max(x)
    #         x = x - x_max
    #         numerator = np.exp(x)
    #         denominator = 1.0 / np.sum(numerator)
    #         x = numerator.dot(denominator)
    #
    #     assert x.shape == orig_shape
    #     return x

    @staticmethod
    def build(width, height, depth, classes):
        """
        （data_format='channels_last'）—input_shape = (128,128,3)代表128*128的RGB图像
        （data_format='channels_first'）—input_shape = (3,128,128)代表128*128的RGB图像
        keras使用tensorflow作为Backend时，格式是（data_format='channels_first'）
        """

        # 不同工具包颜色通道位置可能不一致
        model = Sequential()
        inputShape = (height, width, depth)

        # inputShape = tf.reshape([-1,height, width, depth])
        # 判断chanDim维度具体放在什么位置
        chanDim = -1
        if K.image_data_format() == "channels_first":
            # inputShape = tf.reshape(model1.input_shape,[-1,depth, height, width])
            inputShape = (depth, height, width)
            chanDim = 1

        # 1.创建第一个卷积层
        # CONV => RELU => POOL（创建第一个卷积层，池化层 conv1d一般用于文本数据，conv2d一般用于图像）
        # 在原始图像每3*3特征提取（用非常小的卷积核特征提取，非常多的卷积层特征提取,32个不同的卷积核，权重参数）
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))  # 带权重参数的层都需要连接一个激活函数（全连接层，卷积层）
        model.add(MaxPooling2D(pool_size=(2, 2)))  # 池化：对特征图压缩，损失了一部分特征信息
        # model1.add(Dropout(0.25))

        # 2.可以多次卷积再进行一次池化
        # （CONV => RELU）*3=> POOL
        model.add(Conv2D(64, (3, 3), padding="same", input_shape=inputShape))  # 特征图数量上升，弥补体积压缩的影响
        model.add(Activation("relu"))  # 带权重参数的层都需要连接一个激活函数（全连接层，卷积层）
        # model1.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(128, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        # model1.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        # model1.add(Dropout(0.25))

        # 3.可以多次卷积再进行一次池化
        model.add(Conv2D(128, (3, 3), padding="same", input_shape=inputShape))  # 特征图数量上升，弥补体积压缩的影响
        model.add(Activation("relu"))  # 带权重参数的层都需要连接一个激活函数（全连接层，卷积层）
        # model1.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(128, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        # model1.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        # model1.add(Dropout(0.25))

        # 三维特征图转为1维，神经网络输入是1维的
        # 全连接层将图像转为向量格式
        # FC层
        model.add(Flatten())
        model.add(Dense(512))  # 1024也行
        model.add(Activation("relu"))
        # model1.add(BatchNormalization())
        # model1.add(Dropout(0.8))

        # softmax分类(商品类别）
        model.add(Dense(classes))
        model.add(Activation("softmax"))  # 得到属于每一个类别的概率值，做数据归一化操作

        return model
