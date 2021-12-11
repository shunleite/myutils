# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/11 18:20
@Auth ： 张顺
@No   : 021321712238
@File ：CourseScheduleProvider.py
@IDE ：PyCharm

"""
import math
import random

from faker import Faker


class CourseScheduleProvider:
    def __init__(self):
        self.fake = Faker("zh_CN")
        self.schedulePlan = {"ClassRooms":{},"Teachers":{}}
        self.classRooms = []    # 总共的教室
        self.teachers = []    # 总共的老师
        self.courses = []    # 总共的老师
        self.days = {1:'星期一',2:'星期二',3:'星期三',4:'星期四',5:'星期五',6:'星期六',7:'星期天'}

    def randomCourseSchedules(self, departmentName='计算机学院', teachers=[], classes=[], classRooms=[],courses=[]):
        courseSchedules = {}
        courseScheduleId = 700001
        self.teachers = teachers
        self.classRooms = classRooms
        self.courses = courses
        terms = ['上,第' + str(i) + '学期' if i%2==0  else '下,第' + str(i) + '学期' for i in range(1, 4)]
        termWeeks = [',第' + str(i) + '周' for i in range(1, 17)]
        termDays = [',' + self.days[i] for i in range(1,6)]
        termNodes = [',第' + str(2 * i + 1) + "-" + str(2 * i + 1 + 1) + "节" for i in range(5)]
        # print(terms)
        # print(termWeeks)
        # print(termNodes)
        for classNo in classes:
            for i in range(len(terms)):
                scheduleTimeX = str(int(str(classNo)[:4]) + math.ceil(i/2)) + terms[i]
                schedulePlanX = str(int(str(classNo)[:4]) + math.ceil(i/2)) + terms[i][:1]
                nowCourseTable = self.generaeCourses() # 生成当前学期的课表
                # print("课表: ", )
                for termWeek in termWeeks:
                    scheduleTimeY = scheduleTimeX + termWeek
                    schedulePlanY = schedulePlanX + termWeek
                    nowCourseTableQueue = [i for i in nowCourseTable for x in range(2)]
                    nowCourseTableQueue.extend([0 for i in range(25-len(nowCourseTable)*2)]) # 这个25是len(termDays) * len(termNodes)的长度
                    random.shuffle(nowCourseTableQueue)
                    count = 0
                    # print(nowCourseTableQueue)
                    for termDay in termDays:
                        scheduleTimeZ = scheduleTimeY + termDay
                        schedulePlanZ = schedulePlanY + termDay
                        for termNode in termNodes:
                            scheduleTime = scheduleTimeZ + termNode
                            schedulePlan = schedulePlanZ + termNode
                            if nowCourseTableQueue[count]:
                                # 获取空闲的教室
                                classRoom = self.getFreeClassRoom(schedulePlan)
                                self.schedulePlan["ClassRooms"].get(schedulePlan, []).append(classRoom)
                                # 老师排课时间冲突的情况
                                teacher = self.getFreeTeacher(schedulePlan, nowCourseTable[nowCourseTableQueue[count]])
                                self.schedulePlan["Teachers"].get(schedulePlan, []).append(teacher)
                                courseSchedules[courseScheduleId] = {"courseno":nowCourseTableQueue[count], "classno":classNo, "teacherno":teacher, "scheduletime": scheduleTime,"crno": classRoom}
                                courseScheduleId += 1
                            count += 1
                            # print(scheduleTime)
                            # print(schedulePlan)
        return courseSchedules

    def getFreeClassRoom(self, plan):
        room = None
        while True:
            room = random.choice(list(self.classRooms))
            if room in self.schedulePlan["ClassRooms"].get(plan,[]):
                continue
            break
        return room


    """
    # 选代课老师
    防止一个老师同一时间上两们课，如果存在，则随便找个闲的老师代它的课
    """
    def getFreeTeacher(self, plan, teacher):
        if teacher not in self.schedulePlan["Teachers"].get(plan,[]):
            return teacher
        while True:
            teacher = random.choice(list(self.teachers))
            if teacher in self.schedulePlan["Teachers"].get(plan,[]):
                continue
            break
        return teacher

    def generaeCourses(self):
        randomCount = random.randint(7, 8)
        courses = random.sample(self.courses, randomCount)
        teachers = random.sample(self.teachers, randomCount)
        courseTable = dict(zip(courses,teachers))
        return courseTable




# if __name__ == "__main__":
#     o = CourseScheduleProvider()
#     o.randomCourseSchedules(classes=[202117101, 202117102, 202017101, 202017102])
#


