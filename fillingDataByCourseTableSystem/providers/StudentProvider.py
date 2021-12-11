# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/11 17:01
@Auth ： 张顺
@No   : 021321712238
@File ：StudentProvider.py
@IDE ：PyCharm

"""
import random

from faker import Faker


class StudentProvider:
    def __init__(self):
        self.fake = Faker("zh_CN")

    def randomStudents(self, departmentName='计算机学院',classes={}):
        """

        学号起始位置以 第一个学号：(int)班级号*100 + 1
        递进的格式：下一个学号 = 上一个学号 + 1
        :param departmentName:
        :param classes:
        :param hasStudentsCount:
        :return: {班号:{学号:学生信息}}
        """
        students={}
        for classNo in classes.keys():
            startCno = classNo*100 + 1
            classCount = classes.get(classNo)['classcount']
            # students[classNo] = {}
            while classCount > 0:
                # students[classNo][startCno] = {"studentname": self.fake.name(), "sex": random.randint(0,1),
                students[startCno] = {"studentname": self.fake.name(), "sex": random.randint(0,1),
                                               "birth": str(self.fake.date_between(start_date="-23y", end_date="-19y")),
                                               "department": departmentName,
                                               "classno": classNo,
                                               "address": self.fake.address(),
                                               "phone": self.fake.phone_number(),
                                               "remark": ''
                                               }
                startCno += 1
                classCount -= 1
        return students