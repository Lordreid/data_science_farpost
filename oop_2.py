"""
В этом задании будем улучшать нашу систему классов из задания прошлой лекции
(Student, Teacher, Homework)
Советую обратить внимание на defaultdict из модуля collection для
использования как общую переменную


1. Как то не правильно, что после do_homework мы возвращаем все тот же
объект - будем возвращать какой-то результат работы (HomeworkResult)

HomeworkResult принимает объект автора задания, принимает исходное задание
и его решение в виде строки
Атрибуты:
    homework - для объекта Homework, если передан не этот класс -  выкинуть
    подходящие по смыслу исключение с сообщением:
    'You gave a not Homework object'

    solution - хранит решение ДЗ как строку
    author - хранит объект Student
    created - c точной датой и временем создания

2. Если задание уже просрочено хотелось бы видеть исключение при do_homework,
а не просто принт 'You are late'.
Поднимайте исключение DeadlineError с сообщением 'You are late' вместо print.

3. Student и Teacher имеют одинаковые по смыслу атрибуты
(last_name, first_name) - избавиться от дублирования с помощью наследования

4.
Teacher
Атрибут:
    homework_done - структура с интерфейсом как в словаря, сюда поподают все
    HomeworkResult после успешного прохождения check_homework
    (нужно гаранитровать остутствие повторяющихся результатов по каждому
    заданию), группировать по экземплярам Homework.
    Общий для всех учителей. Вариант ипользования смотри в блоке if __main__...
Методы:
    check_homework - принимает экземпляр HomeworkResult и возвращает True если
    ответ студента больше 5 символов, так же при успешной проверке добавить в
    homework_done.
    Если меньше 5 символов - никуда не добавлять и вернуть False.

    reset_results - если передать экземпряр Homework - удаляет только
    результаты этого задания из homework_done, если ничего не передавать,
    то полностью обнулит homework_done.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""

import datetime
from collections import defaultdict

class DeadlineError(Exception): #Исключение 
    pass

class Person: #Объединяем таким образом Student и Teacher поскольку у них одинаковые атрибуты
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class Homework:
    def __init__(self, text, days):
        self.text = text
        self.deadline = datetime.timedelta(days=days)  # Срок выполнения задания
        self.created = datetime.datetime.now()  # Время создания задания

    def is_active(self): # Проверяем, активно ли задание (не прошёл ли дедлайн)
        return datetime.datetime.now() < self.created + self.deadline

class HomeworkResult:
    def __init__(self, author, homework, solution):
        if not isinstance(homework, Homework):  # Проверяем что homework объект класса Homework
            raise TypeError("You gave a not Homework object")
        self.homework = homework
        self.solution = solution
        self.author = author
        self.created = datetime.datetime.now()

# Класс для студента
class Student(Person):
    def do_homework(self, homework, solution):
        if not homework.is_active():  # Проверяем, активно ли задание
            raise DeadlineError("You are late lol")  # Если нет, выбрасываем исключение
        return HomeworkResult(self, homework, solution)  # Возвращаем результат выполнения

# Класс для учителя
class Teacher(Person):
    homework_done = defaultdict(set)  # Хранилище для выполненных заданий, в виде заранее сделаного словаря "трафарета"

    # Метод для создания домашнего задания
    @staticmethod #Декоратор который превращает метод в функцию (без интеграции)
    def create_homework(task_text, task_days):
        return Homework(task_text, task_days)

    # Метод для проверки домашнего задания
    @classmethod #Принимает ссылку на класс (cls) вместо self
    def check_homework(cls, homework_result):
        if len(homework_result.solution) > 5:  # Проверяем, что решение больше 5 символов
            cls.homework_done[homework_result.homework].add(homework_result)  # Добавляем в homework_done
            return True
        return False

    # Метод для сброса результатов
    @classmethod
    def reset_results(cls, homework=None):
        if homework:
            cls.homework_done.pop(homework, None)  # Удаляем результаты для конкретного задания
        else:
            cls.homework_done.clear()  # Очищаем все результаты


if __name__ == '__main__':
    opp_teacher = Teacher('Daniil', 'Shadrin')
    advanced_python_teacher = Teacher('Aleksandr', 'Smetanin')

    lazy_student = Student('Roman', 'Petrov')
    good_student = Student('Lev', 'Sokolov')

    oop_hw = opp_teacher.create_homework('Learn OOP', 1)
    docs_hw = opp_teacher.create_homework('Read docs', 5)

    result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
    result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
    result_3 = lazy_student.do_homework(docs_hw, 'done')
    try:
        result_4 = HomeworkResult(good_student, "fff", "Solution")
    except Exception:
        print('There was an exception here')
    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done
    assert temp_1 == temp_2

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    print(Teacher.homework_done[oop_hw])
    Teacher.reset_results()
