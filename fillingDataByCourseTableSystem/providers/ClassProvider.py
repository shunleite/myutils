# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/11 16:23
@Auth ： 张顺
@No   : 021321712238
@File ：ClassProvider.py
@IDE ：PyCharm

"""
import datetime
import random

from faker import Faker


class ClassProvider:
    def __init__(self):
        self.fake = Faker("zh_CN")

    def randomClasses(self,departmentName='计算机学院', teachers=[], hasClassCount=4):
        """
        返回随机生成的班级字典（懒得写注释了亲~，自己print/debug看下）
        :param departmentName:
        :param teachers:
        :param hasClassCount: 必须是偶数
        :param classno:
        :return:
        """
        if hasClassCount%2 != 0:
            hasClassCount = 4
        classes = {}
        if not teachers:
            return
        for i in range(2):
            count = hasClassCount/2
            year = (datetime.datetime.now().year if datetime.datetime.now().month >= 9 else datetime.datetime.now().year -1) - i
            classno = int(str(year) + '17101')
            while count > 0:
                classes[classno] = {'department': departmentName, 'classcount': random.randint(39, 45),
                                    # 'enteryear': str(year) + "-09-01",
                                    'enteryear': str(year),
                                    # 'enteryear': year,
                                    'teacherno': random.choice(list(teachers))
                                    }
                classno += 1
                count -= 1
        return classes

        # year = datetime.datetime.now().year if datetime.datetime.now().month >= 9 else datetime.datetime.now().year -1
        # year = random.randint(year - 1,year)
        # # classno = int('213' +  str(year) + '17100')
        # classno = int(str(year) + '17100')
        # while hasClassCount > 0:
        #     classes[classno] = {'department': departmentName, 'classcount': random.randint(39,45),
        #                         'enteryear': str(year) + "-09-01",
        #                         'teacherno': random.choice(list(teachers))
        #                         }
        #     classno += 1
        #     hasClassCount -= 1
        # return classes

