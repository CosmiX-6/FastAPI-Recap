from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Student(models.Model):
    id = fields.IntField(pk = True)
    name = fields.CharField(max_length = 100)
    email = fields.CharField(max_length = 120)
    password = fields.CharField(max_length = 100)
    joined_date = fields.DateField(auto_now_Add = True)
    class Meta:
        pass

Student_Pydantic = pydantic_model_creator(Student, name='stud')
StudentIn_Pydantic = pydantic_model_creator(Student, name = 'studIn', exclude_readonly = True)