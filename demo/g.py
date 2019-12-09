import datetime


class Person(object):

    def __init__(self, name):
        self.name = name
        try:
            lastBlank = name.rindex(' ')
            self.lastName = name[lastBlank + 1:]
        except AssertionError:
            self.lastName = name
        self.birthday = None

    def getName(self):
        return self.name

    def getLastName(self):
        return self.lastName

    def setBirthday(self, birthday):
        self.birthday = birthday

    def getAge(self):
        if self.birthday is None:
            raise ValueError
        return (datetime.date.today() - self.birthday).days

    def __lt__(self, other):
        if self.lastName == other.lastName:
            return self.name < other.name
        return self.lastName < other.lastName

    def __str__(self):
        return self.name


class MITPerson(Person):
    nextIdNum = 0

    def __init__(self, name):
        Person.__init__(self, name)
        self.idNum = MITPerson.nextIdNum
        MITPerson.nextIdNum += 1

    def getIdNum(self):
        return self.idNum

    def isStudent(self):
        return isinstance(self, Student)

    def __lt__(self, other):
        return self.idNum < other.idNum


class Student(MITPerson):
    pass


class UG(Student):

    def __init__(self, name, classYear):
        MITPerson.__init__(self, name)
        self.year = classYear

    def getClass(self):
        return self.year


class Grad(Student):
    pass


class TransferStudent(Student):

    def __init__(self, name, fromSchool):
        MITPerson.__init__(self, name)
        self.fromSchool = fromSchool

    def getOldSchool(self):
        return self.fromSchool


class Grades(object):

    def __init__(self):
        self.students = []
        self.grades = {}
        self.isSorted = True

    def addStudent(self, student):
        if student in self.students:
            raise ValueError('Duplicate student')
        self.students.append(student)
        self.grades[student.getIdNum()] = []
        self.isSorted = False

    def addGrade(self, student, grade):
        try:
            self.grades[student.getIdNum()].append(grade)
        except:
            raise ValueError('Student not in mapping')

    def getGrades(self, student):
        try:
            return self.grades[student.getIdNum()][:]
        except:
            raise ValueError('Student not in mapping')

    def getStudents(self):
        if not self.isSorted:
            self.students.sort()
            self.isSorted = True
        # return self.students[:]
        for s in self.students:
            yield s