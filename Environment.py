'''

本模块主要是搭建环境

'''

import numpy as np
import math

class environment:
    '''
    对信道环境来说，其只会有两个属性，

    1：信道增益 h
    2：等效信道增益 H
    '''
    def __init__(self,distance,SC_Bandwidth):
        self.h = self.__h__(distance)
        self.H = self.__H__(distance,SC_Bandwidth)

    def __wNoise_Power__(self,SC_Bandwidth):
        '''
        求噪声功率
        :param SC_Bandwidth: 子信道的带宽 MHZ
        :return: 噪声功率 单位：w
        '''
        wNoise_Power = (pow(10,(-70+10 * math.log10(SC_Bandwidth * 10e6))/10))/1000
        return wNoise_Power

    def __h__(self,distance):
        '''
        信道增益  路径损耗Loss_path = 3
        :param distance: 距离为***m***
        :return: 信道增益 h
        '''
        Loss_path = 3
        g = math.sqrt(2)*(np.random.random()+np.random.random()*1j)
        h = g*(1/(math.sqrt(pow(distance,Loss_path))))
        return h

    def __H__(self,distance,SC_Bandwidth):
        '''
        求等效信道增益
        :param distance:距离 m
        :param SC_Bandwidth: 子信道带宽
        :return: 等效信道增益
        '''
        h = self.__h__(distance)
        H = pow(abs(h),2)/self.__wNoise_Power__(SC_Bandwidth)
        return H
