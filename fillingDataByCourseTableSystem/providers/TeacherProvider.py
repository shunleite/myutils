# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/11 15:34
@Auth ： 张顺
@No   : 021321712238
@File ：TeacherProvider.py
@IDE ：PyCharm

"""
import random

from faker import Faker
class TeacherProvider:

    def __init__(self,departmentName='计算机学院'):
        self.professionalVa= self.randomProfessional(departmentName='计算机学院')
        self.posts = self.randomPosts()
        self.fake = Faker("zh_CN")

    def randomTeacher(self, departmentName='计算机学院',teacherCount=40, teacherNo=20101):
        """

        :param departmentName: 学院名
        :param teacherCount: 老师数量
        :param teacherNo: 老师编号起始位置
        :return:
        """
        teachers = {}
        while teacherCount > 0:
            teachers[teacherNo] = {'name': self.fake.name(),"department":departmentName,
                                   "professional": random.choice(self.professionalVa),
                                   "post": random.choice(self.posts)}
            teacherCount -= 1
            teacherNo += 1
        return teachers


    def randomProfessional(self,departmentName='计算机学院'):
        randomProfessional = []
        if departmentName=='计算机学院':
            randomProfessional.extend(["Python", "Java", "SQL", "大数据", "云计算", "网络安全"])
        return randomProfessional

    def randomPosts(self):
        return ["教授","副教授","博士"]
