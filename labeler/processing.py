import csv
from .models import Choice, Question



# import data
def getData(filePath):
	with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
        	_, created = Question.objects.get_or_create(
        		question_text = row[0],
        		)
            _, created = Choice.objects.get_or_create(
                choice_text=row[1],
                )