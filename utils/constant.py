from enum import Enum


class UserRole(str,Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class Level(str,Enum):
    jss1 = "jss1"
    jss2 = "jss2"
    jss3 = "jss3"
    sss1 = "jss1"
    sss2 = "sss2"
    sss3 = "sss3"
    
class AnswerOption(str,Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"