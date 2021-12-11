# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/11 17:27
@Auth ： 张顺
@No   : 021321712238
@File ：CourseProvider.py
@IDE ：PyCharm

"""
import random

from faker import Faker


class CourseProvider:
    def __init__(self):
        self.fake = Faker("zh_CN")
        self.courseVariety = [' Python 入门', '面向对象编程（C++ 入门）', '数据结构与算法', '面向对象编程 II（Java 入门）',
                           '离散数学', '自由组队进行程序设计', '计算机体系结构', '数值分析', '形式语言和自动机',
                           '并行运算', '编程原理', '程序语言理论',
                           '操作系统', '计算机网络', '数据库原理 ', '数据库实现', '图形学', '自然语言处理'
                           ]

    def randomCourses(self, departmentName="计算机学院", courseStartNo=1001):
        courses = {}
        count = len(self.courseVariety)
        while count > 0:
            courses[courseStartNo] = {'coursename': self.courseVariety[count-1],
                                      'courseterm': '第' + str(random.randint(1,3)) + "学期",
                                      'termtime': random.randint(13,16),
                                      'termcount': random.randint(3,8)
                                      }

            courseStartNo += 1
            count -= 1
        return courses

