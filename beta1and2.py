'''
这个文件只需要得到beta就行
所以
1：求a
'''
import math
import numpy as np

def f1(P1,H1,Pc,a):
    return math.log2(1+P1*H1)/(Pc+P1) - math.e**(a*P1)

def f2(P1,P2,Pc,H2,a):
    return math.log2(1+(P2*H2)/(1+P1*H2))/(Pc+P2) - math.e**(a*(P2))

def get_a(P,H1,Pc):
    max_ee,max_a = 0,0
    a_list = np.arange(0,10,0.01)

    for a in a_list:
        f = f1(P,H1,Pc,a)
        if f > max_ee:
            max_ee = f
            max_a = a
    return a


def get_beta(Pn,Pc,H1,H2):
    a = get_a(Pn,H1,Pn)

    Itertion = int(input('输入迭代次数：'))
    sita = float(input('输入sita：'))

    def argP1(p_low,p_high,H1):
        max_ee,max_p = 0,0
        for i in range(p_low,p_high):
            temp_ee = f1(i,H1,Pc,a)
            if temp_ee > max_ee:
                max_p = i
                max_ee = temp_ee
        return max_p

    def P2_range(p1,p2):
        if p1 + p2 <= Pn:
            low_P2 = math.sqrt((Pc * (1 + p1 * H2)) / H2)
            temp_P2 = Pn - p1
            if temp_P2 >= low_P2:
                return low_P2, temp_P2
            else:
                raise ValueError('P2的空间条件不符合')
        else:
            raise ValueError('P1+P2 > Pn，range_P2处')

    def argP2(p1,p2_low,p2_high):
        max_ee,max_p = 0,0
        for i in range(p2_low,p2_high):
            temp_ee = f2(p1,i,Pc,H2,a)
            if temp_ee > max_ee:
                max_ee = temp_ee
                max_p = i
        return max_p

    def P1_range(p1,p2):
        if p1 + p2 <= Pn:
            p1_low = 0
            p1_high = p2**2/Pc - 1/H2
            temp_p1 = Pn - p2
            if temp_p1 >= p1_high:
                return p1_low, p1_high
            else:
                raise ValueError('P1的空间条件不符合')
        else:
            raise ValueError('P1+P2 > Pn rang_P1处')


    p1_low,p1_high = 0,Pn
    pre_p1 = 0
    p2 = math.sqrt((Pc*(1+p1_low*H2))/H2)
    k = 0
    while k <= Itertion:
        p1 = argP1(p1_low,p1_high,H1)
        p2_low,p2_high = P2_range(p1,p2)
        p2 =argP2(p1,p2_low,p2_high)
        p1_low,p1_high = P1_range(p1,p2)
        if p1 - pre_p1 < sita:
            break
        else:
            pre_p1 = p1
        k+=1
    beta1,beta2 = p1/Pn,p2/Pn
    return beta1,beta2


