from datetime import date, datetime, timedelta
from random import randint, choice
import faker 
from sqlalchemy import select

from database.models import Teacher, Student, Discipline, Grade, Group
from database.db import session


def date(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def data():
    disciplines = [
        "Системний аналіз",
        "Теоретична механіка",
        "Математичний аналіз",
        "Алгебра",
        "Аналітична геометрія",
        "Креслення"
    ]

    groups = ['А-1', 'А-2', 'А-3']

    fake = faker.Faker()
    number_teachers = 5
    number_students = 50

    def seed_teachers():
        for _ in range(number_teachers):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        teacher_i = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_i)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_students():
        group_i = session.scalars(select(Group.id)).all()
        for _ in range(number_students):
            student = Student(fullname=fake.name(), group_id=choice(group_i))
            session.add(student)
        session.commit()

    def seed_grades():
        start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-05-25", "%Y-%m-%d")
        d_range = date(start=start_date, end=end_date)
        discipline_ids = session.scalars(select(Discipline.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range:
            random_id_discipline = choice(discipline_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]

            for student_id in random_ids_student:
                grade = Grade(
                    grade=randint(2, 5),
                    date_of=d,
                    student_id=student_id,
                    discipline_id=random_id_discipline,
                )
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    data()
