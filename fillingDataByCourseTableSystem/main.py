# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/11 15:02
@Auth ： 张顺
@No   : 021321712238
@File ：main.py
@IDE ：PyCharm

"""
import json
import time

from faker import Faker

from fillingDataByCourseTableSystem.providers.ClassProvider import ClassProvider
from fillingDataByCourseTableSystem.providers.ClassRoomProvider import ClassRoomProvider
from fillingDataByCourseTableSystem.providers.CourseProvider import CourseProvider
from fillingDataByCourseTableSystem.providers.CourseScheduleProvider import CourseScheduleProvider
from fillingDataByCourseTableSystem.providers.StudentProvider import StudentProvider
from fillingDataByCourseTableSystem.providers.TeacherProvider import TeacherProvider

departments = {"计算机学院":""} # 院系:(班级1,班级1,...)
if __name__ == "__main__":
    fake = Faker("zh_CN")
    data = {"老师表内容":{},"学生表内容":{},"班级表内容":{}}
    table = {"老师表内容":('teachers', 'teacherno'),
             "学生表内容":('students', 'studentno'),
             "班级表内容":('classes', 'classno'),
             "课程表内容":('courses', 'courseno'),
             "教室信息内容":('classroom', 'crno'),
             "课表信息内容":('courseschedule', 'scheduleid'),
             }
    """
        第一步: 生成老师表内容
    """
    teacherProvider = TeacherProvider()
    teachers = teacherProvider.randomTeacher(departmentName="计算机学院", teacherCount=40)
    # print("老师表内容：", json.dumps(teachers))
    data['老师表内容'] = teachers
    """
        第二步: 生成班级
    """
    classProvider = ClassProvider()
    classes = classProvider.randomClasses(departmentName='计算机学院',teachers=teachers.keys(), hasClassCount=4)
    # print("班级表内容：", classes)
    # print("班级表内容：", json.dumps(classes))
    data['班级表内容'] = classes
    """
        第三步: 生成学生信息
    """
    studentProiver = StudentProvider()
    students = studentProiver.randomStudents(departmentName='计算机学院',classes=classes)
    # print("学生表：",json.dumps(students))
    # print("学生表内容：",json.dumps(students))
    data['学生表内容'] = students

    """
        第四步: 生成课程信息
    """
    courseProvider = CourseProvider()
    courses = courseProvider.randomCourses(departmentName='计算机学院')
    # print("课程表内容：", json.dumps(courses))
    data['课程表内容'] = courses

    """
        第五步：生成教室信息
    """
    classRoomProvider = ClassRoomProvider()
    classRooms = classRoomProvider.randomClassRooms()
    # print("教室信息内容：", json.dumps(classRooms))
    data['教室信息内容'] = classRooms

    """
        第六步：生成课程表信息
    """
    courseScheduleProvider = CourseScheduleProvider()
    courseSchedules = courseScheduleProvider.randomCourseSchedules(departmentName='计算机学院', teachers=teachers.keys(), classes=classes.keys(), classRooms=classRooms.keys(),courses=courses.keys())
    # print("课表信息内容：", json.dumps(courseSchedules,ensure_ascii=False))
    data['课表信息内容'] = courseSchedules
    # print(json.dumps(data, ensure_ascii=False))
    
    # 此处为SQL格式修改

    databaseFormat = """

CREATE TABLE IF NOT EXISTS `users`(
	`username` VARCHAR(50) NOT NULL PRIMARY KEY,
	`password` VARCHAR(50) NOT NULL,
	`variety` VARCHAR(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS  `students` (
	`studentno` VARCHAR(50) NOT NULL PRIMARY KEY,
	`studentname` VARCHAR(50) NOT NULL ,
	`sex` bit(1) NOT NULL COMMENT '0为女，1为男',
	`birth` datetime NOT NULL,
	`department` VARCHAR(50) NOT NULL,
	`classno` VARCHAR(50) NOT NULL,
	`address` VARCHAR(100) NOT NULL,
	`phone` VARCHAR(50) NOT NULL,
	`remark` text
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS  `teachers` (
	`teacherno` VARCHAR(50) NOT NULL PRIMARY KEY,
	`teachername` VARCHAR(50) NOT NULL,
	`department` 	VARCHAR(50) NOT NULL,
	`professional` VARCHAR(50) NOT NULL,
	`post` VARCHAR(50) NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS  `classes` (
	`classno` VARCHAR(50) NOT NULL PRIMARY KEY,
	`department` VARCHAR(50) NOT NULL,
	`classcount` BIGINT(6) NOT NULL,
	`enteryear` datetime NOT NULL,
	`teacherno` VARCHAR(50) NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS  `courses` (
	`courseno` VARCHAR(50) NOT NULL PRIMARY KEY,
	`coursename` VARCHAR(50) NOT NULL,
	`courseterm` VARCHAR(50) NOT NULL,
	`termtime` BIGINT(5) 	NOT NULL,
	`termcount` BIGINT(5) NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS  `classroom`(
	`crno` VARCHAR(50) NOT NULL PRIMARY KEY,
	`capacity` BIGINT(5) NOT NULL,
	`ismedia` bit(1) NOT NULL COMMENT '0为否 1为是',
	`status` bit(1) NOT NULL COMMENT '0为未占用 1为已占用'
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS  `courseschedule`(
	`scheduleid` VARCHAR(50) NOT NULL PRIMARY KEY,
	`courseno` VARCHAR(50) NOT 	NULL,
	`classno` VARCHAR(50) NOT NULL,
	`teacherno` VARCHAR(50) NOT NULL,
	`scheduletime` VARCHAR(50) NOT NULL,
	`crno` VARCHAR(50) NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

-- 为每个学生自动创建user账户，账户为:学号，初始密码为：学号后6位
CREATE TRIGGER insert_user_students
AFTER INSERT ON `students`
FOR EACH ROW
INSERT INTO `users`
SELECT NEW.studentno, MD5(RIGHT(NEW.studentno,6)),'student';

-- 为每个老师自动创建user账户，账户为:编号，初始密码为：编号后6位
CREATE TRIGGER insert_user_teachers
AFTER INSERT ON `teachers`
FOR EACH ROW
INSERT INTO `users`
SELECT NEW.teacherno, MD5(RIGHT(NEW.teacherno,6)),'teacher'; -- 学号后六位为密码

-- DROP TRIGGER insert_user_teachers;
-- DROP TRIGGER insert_user_students;

-- 添加一个超级管理员
INSERT INTO `users` VALUES('root',MD5('root'),'admin');
"""

    for item in data.keys():
        nowTable = table[item][0]
        nowPriId = table[item][1]
        for info in data[item].keys():
            strs = ""
            for ov in data[item][info].keys():
                if data[item][info][ov] == 1 or data[item][info][ov] == 0:
                    strs += ", " + str(data[item][info][ov])
                else:
                    strs += ", '" + str(data[item][info][ov]) + "'"
            databaseFormat += "insert into `" + str(nowTable) + "` select '" + str(info) + "'" + strs + ";\n"
    print(databaseFormat)

    ## 输入到sql里：
    with open("test.sql", "w+",encoding="utf-8") as f:
        f.writelines(databaseFormat)


    # print(fake.name_male())
    # print(fake.phone_number())
    # print(fake.address())
    # print(fake.name_female())
    # while True:
    #     print(fake.date_between(start_date="-23y", end_date="-19y"))
    #     time.sleep(0.2)
    # s = fake.simple_profile(sex="M")
    # for i, v in s.items():
    #     print(i, v)
    # for k,v in fake.simple_profile(sex='m').items():
    #     print(k,v)