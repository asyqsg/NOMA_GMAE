import Environment
import Progaming
import numpy as np
'''
根据论文所述
1：需要获得一个H的矩阵

'''

#用户数目
user_number = 4

#每个信道的用户数目
users_prechannel = 2

# 带宽 MHZ
BandWidth = 5

# 信道数目
band_number = user_number/users_prechannel

# 每个信道的带宽
SC_bandwidth = BandWidth/band_number


def H_and_h(user_number,band_number):
    '''
    产生H和h的函数
    :param user_number: 用户数目
    :param band_number: 信道数目
    :return: H和h
    '''
    # H是一个矩阵
    H = np.zeros([user_number, band_number])
    h = np.zeros([user_number, band_number])
    # 产生每一个H的区别在于其距离，所有要生成其距离
    for i in range(user_number):
        distance = (500 - 50) * np.random.random_sample() + 50  # 距离是在50-500m中的任意一个位置
        for j in range(band_number):
            user_channel = Environment.environment(distance, SC_bandwidth)
            H[i][j] = user_channel.H
            h[i][j] = user_channel.h
    return H,h

