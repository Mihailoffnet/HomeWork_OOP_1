class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_hw(self, lecturer, course, lecturer_grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.lecturer_grades:
                lecturer.lecturer_grades[course] += [lecturer_grade]
            else:
                lecturer.lecturer_grades[course] = [lecturer_grade]
        else:
            return 'Ошибка'    

    def _rate_s(self, grades):
        list = []
        for value in grades.values():
            list += value
        if len(list) == 0: # без этой проверки при вызове метода до выставления оценок код падает с делением на ноль
            result_s = 0
        else:
            result_s = round(sum(list)/len(list), 1)
        return result_s
        
    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self._rate_s(self.grades)}\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}\nЗавершенные курсы: {", ".join(self.finished_courses)}'
        return res

    def compare_rate_s (self, student):
        if not isinstance(student, Student): # проверка является ли объект экземпляром указанного класса
            return
        if student._rate_s(student.grades) < self._rate_s(self.grades):
            print(f'Средний балл {self.name} {self.surname} - {self._rate_s(self.grades)}, это больше, чем {student._rate_s(student.grades)} у {student.name} {student.surname}')
        elif student._rate_s(student.grades) == self._rate_s(self.grades):
            print(f'У {self.name} {self.surname} и {student.name} {student.surname} одинаковый средний балл {self._rate_s(self.grades)}')
        else:
            print(f'Средний балл {self.name} {self.surname} - {self._rate_s(self.grades)}, это меньше, чем {student._rate_s(student.grades)} у {student.name} {student.surname}')  
        
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lecturer_grades = {}

    def _rate_l(self, lecturer_grades):
        # average = f'self: {self} lecturer_grades: {lecturer_grades}'
        list = []
        for value in lecturer_grades.values():
            list += value
        if len(list) == 0: 
            result_l = 0
        else:
            result_l = round(sum(list)/len(list), 1)
        return result_l
            
    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self._rate_l(self.lecturer_grades)}'
        return res

class Reviewer(Mentor):

    def rate_hw(self, student, course, grade): # по правильному этому методу лучше дать другое название, не как у оценки студентов лекторам? Хотя по приоритету сработает и так правильно.
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
        
    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res

# Создаем объект класса "Лучший студент" и назначаем курсы, которые он изучает
best_student = Student('Viktor', 'Mikhaylov', 'M')
best_student.courses_in_progress += ['Python from zero'] # или лучше сразу указать все курсы? ['Python from zero', 'GIT', 'OOP'] 
best_student.courses_in_progress += ['OOP']
best_student.finished_courses += ['GIT']

# Создаем объект класса "Другой студент" и назначаем курсы, которые он изучает
another_student = Student('Another', 'Student', 'M')
another_student.courses_in_progress += ['GIT']
another_student.courses_in_progress += ['OOP']
another_student.finished_courses += ['Python from zero']

# Создаем объект "Крутой проверяющий" и назначаем курсы, которые он проверяет, выставляем оценки студентам
cool_reviewer = Reviewer('Alexandr', 'Bardin')
cool_reviewer.courses_attached += ['OOP']
cool_reviewer.courses_attached += ['Python from zero']
cool_reviewer.courses_attached += ['GIT']
cool_reviewer.rate_hw(best_student, 'OOP', 7) 
cool_reviewer.rate_hw(best_student, 'Python from zero', 9)
cool_reviewer.rate_hw(best_student, 'Python from zero', 8)
cool_reviewer.rate_hw(another_student, 'OOP', 6) 
cool_reviewer.rate_hw(another_student, 'GIT', 8)
cool_reviewer.rate_hw(another_student, 'GIT', 7)

# Создаем объект "другой проверяющий" и назначаем курсы, которые он проверяет, выставляем оценки студентам
another_reviewer = Reviewer('Another', 'Reviewer')
another_reviewer.courses_attached += ['GIT']
another_reviewer.courses_attached += ['OOP']
another_reviewer.rate_hw(another_student, 'GIT', 6) 
another_reviewer.rate_hw(another_student, 'GIT', 8)
another_reviewer.rate_hw(another_student, 'OOP', 7)
another_reviewer.rate_hw(best_student, 'GIT', 10) # Оценка не выставится, так как курс студентом уже закончен
another_reviewer.rate_hw(best_student, 'GIT', 8)
another_reviewer.rate_hw(best_student, 'OOP', 9)

# Создаем объект "Крутой лектор" и назначаем курсы, которые он преподает, выставляем ему оценки
cool_lecturer = Lecturer('Oleg', 'Bulygin')
cool_lecturer.courses_attached += ['Python from zero']
cool_lecturer.courses_attached += ['OOP']
best_student.rate_hw(cool_lecturer, 'OOP', 10)
best_student.rate_hw(cool_lecturer, 'GIT', 10) # оценка не добавится, так как курс студентом уже закончен, и лектор его не преподает, сработает проверка первого из этих двух условий
best_student.rate_hw(cool_lecturer, 'Python from zero', 9)
best_student.rate_hw(cool_lecturer, 'Python from zero', 10)
another_student.rate_hw(cool_lecturer, 'OOP', 8)
another_student.rate_hw(cool_lecturer, 'Python from zero', 8)

# Создаем объект "Другой лектор" и назначаем курсы, которые он преподает, выставляем ему оценки
another_lecturer = Lecturer('Another', 'Lecturer')
another_lecturer.courses_attached += ['GIT','Python from zero']
best_student.rate_hw(another_lecturer, 'Python from zero', 8)
best_student.rate_hw(another_lecturer, 'Python from zero', 9)
best_student.rate_hw(another_lecturer, 'GIT', 10) 
another_student.rate_hw(another_lecturer, 'GIT', 8)
another_student.rate_hw(another_lecturer, 'OOP', 8)

print()
print('Лучший студент')
print(best_student)

print()
print('Другой студент')
print(another_student)

print()
print('Крутой проверяющий')
print(cool_reviewer)
# print(f' Словарь крутой проверяющий: {cool_reviewer.__dict__}')
# print(f'Оценки лучшему студенту: {best_student.grades}')
# print(f'Оценки другому студенту: {another_student.grades}')

print()
print('Другой проверяющий')
print(another_reviewer)
# print(f'Оценки лучшему студенту: {best_student.grades}')
# print(f'Оценки другому студенту: {another_student.grades}')

print()
print('Крутой Лектор')
print(cool_lecturer)
# print(f'Лектор ведет курсы: {cool_lecturer.courses_attached}')
# print(f'Оценки крутому лектору: {cool_lecturer.lecturer_grades}')

print()
print('Другой лектор')
print(another_lecturer)
# print(f'Лектор ведет курсы: {another_lecturer.courses_attached}')
# print(f'Оценки другому лектору: {another_lecturer.lecturer_grades}')

print()
best_student.compare_rate_s(another_student)
print()
another_student.compare_rate_s(best_student)
