"""
关于信道分配

matched:list   已经得到匹配的用户
unmatched：list   还没有得到匹配的用户

需要的输入：
user_list: 用户的列表
user_number: 用户数目
channel_number: 信道数目

H: H是用户数目*信道数目的矩阵

"""

import numpy as np

import Energy_E

#算法1
def EE():
    return 0



#算法2
def matching(users_prechannel,user_number:int,channel_number:int,user_list:list,H:np):

    # 没有匹配的
    unmatched = [i for i in range(user_number)]

    # 能效列表
    ee_list = [0 for i in range(channel_number)]

    # 没有匹配的
    matched = np.zeros([user_number,users_prechannel])



    while unmatched:
        for i in range(user_number):

            max_Hi = max(H[i])
            choose_channel = H[i].index(max_Hi)




