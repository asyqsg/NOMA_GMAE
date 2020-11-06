"""
文章中的算法
"""
import sys
import numpy as np
import math

import Game_Theory

sita = 0.01  #迭代跳出条件
#迭代次数
iteration = int(input("输入迭代次数："))
users_prechannel = int(input("每个子载波上用户数目:"))


#算法1  NE for Super-Modular Game
#这是为了求比例，所以还是不需要总的Pn



def ee_subchannel(H1,H2,Pc,Pn):
    #初始化功率

    P1 = 0
    P2 = math.sqrt((Pc*(1+P1*H2))/H2)

    # 在计算EE前需要先确定a的值
    def get_a(users_prechannel):
        '''
        确定a的值   采用全局搜索的方法
        :param users_prechannel:每个信道的用户数目
        :return: 返回最大ee时的a
        '''

        if users_prechannel > 2:
            raise Exception('每个子载波上的用户数不对')

        # 每个用户的功率都为1
        P_user = 1
        # a的范围为0~10
        max_ee = 0
        a_get = 0

        a_list = np.arange(0, 10, 0.01)
        for a in a_list:
            f1 = (math.log2(1 + P_user * H1)) / (Pc + P_user) - math.e ** (a * P_user)
            f2 = (math.log2(1 + (P_user * H2) / (1 + P_user * H2))) / (Pc + P_user) - math.e ** (a* P_user)
            sum_ee = f1 + f2
            if sum_ee > max_ee:
                max_ee = sum_ee
                a_get = a

        return a_get

    #能效 f1 and  h2
    def f1(p1,H1):
        ee_f1 = (math.log2(1 + p1 * H1)) / (Pc + p1) - math.e ** (get_a(users_prechannel) * p1)
        return ee_f1
    def f2(p1,p2,H2):
        ee_f2 = (math.log2(1 + (p2 * H2) / (1 + p1 * H2))) / (Pc + p2) - math.e ** (get_a(users_prechannel) * p2)
        return ee_f2


    def P1_argmaxByf1(low,high,H1):
        max_ee,max_p = 0,0
        for i in range(low,high):
            temp_ee = f1(i,H1)
            if max_ee < temp_ee:
                max_ee = temp_ee
                max_p = i
        return max_p

    def range_P2(P1,P2,H2):
        if P1+P2 <= Pn:
            low_P2 = math.sqrt((Pc*(1+P1*H2))/H2)
            temp_P2 = Pn - P1
            if temp_P2 >= low_P2:
                return low_P2,temp_P2
            else:
                raise ValueError('P2的空间条件不符合')
        else:
            raise ValueError('P1+P2 > Pn，range_P2处')

    def P2_argmaxByf2(P1,P2_low,P2_high,H2):
        max_ee,max_p = 0,0
        for i in range(P2_low,P2_high):
            temp_ee = f2(P1,i,H2)
            if max_ee < temp_ee:
                max_ee = temp_ee
                max_p = i
        return max_p

    def range_P1(P1,P2,H2):
        if P1+P2 <= Pn:
            P1_low = 0
            P1_high = P2**2/Pc - 1/H2
            temp_P1 = Pn - P2
            if temp_P1 >= P1_high:
                return P1_low,P1_high
            else:
                raise ValueError('P1的空间条件不符合')
        else:
            raise ValueError('P1+P2 > Pn rang_P1处')



    k = 0
    pre_p1= 0
    P1_high,P1_low = Pn,0
    # 由于其是求百分数，所以其功率范围设置为0~1000
    while k <= iteration:

        P1 = P1_argmaxByf1(P1_low,P1_high,H1)
        P2_low, P2_high = range_P2(P1, P2, H2)
        P2 = P2_argmaxByf2(P1, P2_low, P2_high, H2)
        P1_low, P1_high = range_P1(P1, P2, H2)
        if P1 - pre_p1 < sita:
            break
        else:
            pre_p1 = P1

        k+=1
    beta_1,beta_2 = P1/Pn,P2/Pn
    return beta_1,beta_2



#算法2
def matching(users_prechannel:int,user_number:int,H:np,Pc,Pn) -> np:

    channel_number = user_number//users_prechannel

    # 没有匹配的
    unmatched = [i for i in range(user_number)]

    # 能效列表
    ee_list = [0 for i in range(channel_number)]

    # 没有匹配的
    matched = np.zeros([channel_number,users_prechannel])

    while unmatched:
        user_list = unmatched
        for i in range(user_number):

            #由于不对动态数字，所以用了两个数组在每次循环后对其添加
            removed = []
            add = []

            # 找到每一个用户（每一行）的最匹配的信道
            channel_index = np.argmax(H[i])
            H_choose = H[i][channel_index]

            if users_prechannel != 2:
                raise Exception('完善大于2用户的情况')
            else:
                if matched[channel_index][0] == matched[channel_index][1] == 0:
                    #此信道为空
                    matched[channel_index][0] = [H_choose,i] #[H,用户编号]
                    removed.append(i)
                elif matched[channel_index][0] != 0 and matched[channel_index][1] ==0:
                    matched[channel_index][1] = [H_choose,i]
                    removed.append(i)
                else:
                    #此时是信道已经满了，需要根据算法1进行比较
                    #将三个用户，三种信道增益放入算法1内，得到最优的用户情况

                    #have_choosed = [[H,i][H,i]]
                    have_choosed = [matched[channel_index][0],matched[channel_index][1]]

                    #将出问题的用户标号放入remove列表
                    removed.append(have_choosed[0][1])
                    removed.append(have_choosed[1][1])

                    #wantBechoosed - [H,i]
                    wantBechoosed = [H_choose,i]

                    #group = [[H,i],[H,i]]
                    group1 = sorted(have_choosed,key=lambda x:x[0],reverse=True)
                    group2 = [have_choosed[0],wantBechoosed]
                    group2 = sorted(group2,key=lambda x:x[0],reverse=True)
                    group3 = [have_choosed[0],wantBechoosed]
                    group3 = sorted(group3,key=lambda x:x[0],reverse=True)

                    #[[H,i],[],[]]
                    Gaming = [group1,group2,group3]
                    Gaming_ee = []
                    for i in Gaming:
                        game_ee = ee_subchannel(i[0][0],i[1][0],Pc,Pn)
                        Gaming_ee.append(game_ee)
                    max_ee = max(Gaming_ee)
                    wanted_group = Gaming[Gaming_ee.index(max_ee)]

                    #注意：数据类型可能不同
                    matched[channel_index] = wanted_group

                    add.append(wanted_group[0][1])
                    add.append(wanted_group[1][1])

        for i in removed:
            user_list.remove(i)
        for i in add:
            user_list.append(i)
        user_list.sort()
        unmatched = user_list
    return matched


#算法3
# pre_Pn,cur_Pn = 0,1
#
# def program_3(Pc,H_matched,Bs,P):
#     Pn_arange = np.arange(0,P,0.1)
#     def get_Pn()
#     k = 0
#     while k <= iteration and abs(pre_Pn - cur_Pn) > sita:









