'''
计算能效的所有函数
'''
import math
import numpy as np

class GameTheory:
    def get_a(self,H1,Pn,Pc):
        if not H1 or not Pn or not Pc:
            raise Exception('缺少必要条件')
        else:

            R = math.log2(1+Pn*H1)
            chu = Pc+Pn
            pre = R/chu
            def get_penalty(a):
                penalty_func = math.e**(a*Pn)
                return penalty_func

            a = np.arange(0,10,0.01)
            max_ee,max_a = 0,0
            for i in a:
                f_pen = pre - get_penalty(i)
                if f_pen > max_ee:
                    max_ee = f_pen
                    max_a = i
        return max_a
