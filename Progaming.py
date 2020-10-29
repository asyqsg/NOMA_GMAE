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
import sys
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
    matched = np.zeros([channel_number,users_prechannel])



    while unmatched:
        for i in range(user_number):

            # 找到每一个用户（每一行）的最匹配的信道
            channel_index = np.argmax(H[i])
            H = H[i][channel_index]

            if users_prechannel != 2:
                print('完善大与2的情况')
                sys.exit()
            else:
                if matched[channel_index][0] == matched[channel_index][1] == 0:
                    #此信道为空
                    matched[channel_index][0] = [H,i] #[H,用户编号]
                    unmatched.remove(i)
                elif matched[channel_index][0] != 0 and matched[channel_index][1] ==0:
                    matched[channel_index][1] = [H,i]
                    unmatched.remove(i)
                else:
                    #此时是信道已经满了，需要根据算法1进行比较
                    [[H,i]]







