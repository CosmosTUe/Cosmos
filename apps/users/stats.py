import matplotlib.pyplot as plt
from django.db.models import Count, Case, When, Value, BooleanField, F, CharField
from django.db.models.functions import ExtractMonth, ExtractYear, Concat

from apps.users.models.profile import Profile

def get_date_joined_stats(query):
    EU_NATIONALITIES = ["Austrian", "Belgian", "Bulgarian", "Croatian", "Cypriot", "Czech",
                        "Danish", "Dutch", "Estonian", "Finnish", "French", "German", "Greek",
                        "Hungarian", "Icelander", "Irish", "Italian", "Latvian", "Liechtensteiner",
                        "Lithuanian", "Luxembourger", "Maltese", "Norwegian", "Polish", "Portuguese",
                        "Romanian", "Slovakian", "Slovenian", "Spanish", "Swedish"]


    # Takes an academic year as July 1-June 30th, coinciding with a board year,
    # makes a list with other relevant data
    date_joined_list = query.annotate(month=ExtractMonth('user__date_joined'), year=ExtractYear('user__date_joined'),
            academic_start_year=Case(
                When(month__gte=7, then=F('year')),                     
                default=F('year') - 1                                   
            ),
            academic_end_year=Case(
                When(month__gte=7, then=F('year') + 1),
                default=F('year')
            ),
            academic_year=Concat(
                F('academic_start_year'),
                Value('–'),
                F('academic_end_year'),
                output_field=CharField()
            ),
            is_eu=Case(
                When(nationality__in=EU_NATIONALITIES, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).values('academic_year', 'institutiontue__program', 'is_eu'
                 ).annotate(count=Count('id')
                            ).order_by('academic_year', 'institutiontue__program', 'is_eu')

    # Turn the list of dictionaries into one dictionary
    date_joined = {f"{item['academic_year']} | {item['institutiontue__program']} | {'EU' if item['is_eu']else 'Non-EU'}": item['count']
                   for item in date_joined_list}

    # Call the plotting function (used in case the plotting function wants to be changed)
    plots = [make_plot(date_joined, 'AON wanted this data ONLY TUE STUDENTS HERE tho tbf thats by far the vast majority')]
    return plots

def get_nationality_stats(query):
    # Creates a list of dictionaries of the nationalities and their count
    nationality_list = query.values("nationality").annotate(Count("nationality"))

    # Turn the list of dictionaries into one dictionary
    nationality = {item["nationality"]: item["nationality__count"] for item in nationality_list}

    # Call the plotting function (used in case the plotting function wants to be changed)
    plots = [make_plot(nationality, "nationality")]
    return plots


def get_major_stats(query):
    department_list = query.values("department").annotate(Count("department"))
    program_list = query.values("program").annotate(Count("program"))

    # Turn the list of dictionaries into one dictionary
    department = {item["department"]: item["department__count"] for item in department_list}
    program = {item["program"]: item["program__count"] for item in program_list}

    # Call the plotting function (used in case the plotting function wants to be changed)
    plots = [make_plot(department, "department"), make_plot(program, "program")]
    return plots


def make_plot(data, name):
    # Makes a plot from the data and then returns the location of where it's saved
    filepath = "/tmp/" + name + "-graph.jpg"
    plt.figure(1, [20, 8])
    rects = plt.bar(data.keys(), data.values())
    plt.title(name.capitalize())
    plt.xticks(rotation=45, ha="right")

    # Attach a text label above each bar displaying its height
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filepath
