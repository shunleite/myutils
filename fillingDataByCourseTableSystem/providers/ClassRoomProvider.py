# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/11 18:03
@Auth ： 张顺
@No   : 021321712238
@File ：ClassRoomProvider.py
@IDE ：PyCharm

"""
import random

from faker import Faker


class ClassRoomProvider:
    def __init__(self):
        self.fake = Faker("zh_CN")

    def randomClassRooms(self):
        """
        教室的格式
        :return:
        """
        classRooms = {}
        for i in range(1,3):    # 几楼
            for j in range(1,7):    # 几层
                for t in range(1,8): # 几间
                    crno = i*1000 + j*100 + t
                    classRooms[crno] = {'capacity': random.choice([50,80,80,80,80,80,160,160,160,300]),
                                        'ismedia': random.choice([0,1,1]),
                                        'status': 0 # 默认为未占用0
                                        }

        return classRooms

if __name__ == "__main__":
    t = ClassRoomProvider();
    t.randomClassRooms()
