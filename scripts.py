import random
import sys

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation

COMMENDATION_TEXTS = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
    ]

def get_child(schoolkid='Фролов Иван'):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
        return child
    except MultipleObjectsReturned:
        sys.exit('Учеников с таким именем больше одного')
    except ObjectDoesNotExist:
        sys.exit('Такого ученика нет в школе')


def fix_marks(schoolkid='Фролов Иван'):
    child = get_child(schoolkid)
    bad_marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid='Фролов Иван'):
    child = get_child(schoolkid)
    chastisements = Chastisement.objects.filter(schoolkid=child)
    for chastisement in chastisements:
        chastisement.delete()


def create_commendation(schoolkid='Фролов Иван', subject_title='Музыка'):
    child = get_child(schoolkid)
    subject = Subject.objects.get(title=subject_title, year_of_study=child.year_of_study)
    lesson = Lesson.objects.filter(year_of_study=child.year_of_study,
                                   group_letter=child.group_letter,
                                   subject=subject).order_by('date').last()
    commendation_text = random.choice(COMMENDATION_TEXTS)
    Commendation.objects.create(text=commendation_text, created=lesson.date,
                                schoolkid=child, subject=subject, teacher=lesson.teacher)
