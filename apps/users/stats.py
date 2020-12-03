from django.db.models import Count
import matplotlib.pyplot as plt

# Profile.objects.values('nationality').annotate(Count('nationality'))
# dict = {nat[item]['nationality']:nat[item]['nationality__count'] for item in data]


def getStats(query):

    # Creates a list of dictionaries of the nationalities and their count
    departmentList = query.values("department").annotate(Count("department"))
    programList = query.values("program").annotate(Count("program"))
    nationalityList = query.values("nationality").annotate(Count("nationality"))

    # Turn the list of dictionaries into one dictionary
    department = {item["departement"]: item["department__count"] for item in departmentList}
    program = {item["program"]: item["program__count"] for item in programList}
    nationality = {item["nationality"]: item["nationality__count"] for item in nationalityList}

    # Call the plotting function (used in case the plotting function wants to be changed)
    makePlot(department)
    makePlot(program)
    makePlot(nationality)


def makePlot(data):

    plt.bar(data)
