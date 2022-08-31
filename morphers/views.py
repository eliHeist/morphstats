from django.shortcuts import render
from django.views.generic import ListView, DetailView
from morphers.filters import MorpherFilter
import xlwt
from django.http import HttpResponse

from morphers.models import Grade, Morpher
from stats.models import Day
from stats.views import Counter, getPresent



# Create your views here.
class MorpherListView(ListView):
    model = Morpher
    context_object_name = 'morphers'
    template_name = "morphers/list.html"

def morpherListView(request):
    morphers = Morpher.objects.all()
    counter = Counter()
    template_name = "morphers/list.html"

    context = {
        'morphers':morphers,
        'counter':counter,
    }
    return render(request, template_name, context)

def attendanceStatus(object, days):
    dayz = []
    for day in days:
        present = getPresent(day)
        if object in present:
            dayz.append({'date':day.date.strftime('%A %d, %B %Y'),'status':'Present'})
        else:
            dayz.append({'date':day.date.strftime('%A %d, %B %Y'),'status':'Absent'})
    return dayz


class MorpherDetailView(DetailView):
    model = Morpher
    context_object_name = 'morpher'
    template_name = "morphers/detail.html"

    def get_context_data(self, **kwargs):
        context = super(MorpherDetailView, self).get_context_data(**kwargs)
        days = Day.objects.all().order_by('-date')[:5]
        dayz = attendanceStatus(self.object, days)
        

        context['days'] = dayz
        return context

# generate view not working right
def generateDocs(request):
    template_name = "morphers/generate.html"
    morphers = Morpher.objects.all()
    filter1 = MorpherFilter(request.GET, queryset=morphers)
    morphers = filter1.qs

    context = {
        'filter1':filter1,
        'morphers':morphers,
    }
    return render(request, template_name, context)

def exportExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Candidates') # this will make a sheet named Candidates

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Class', 'School']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Morpher.objects.filter(grade__is_candidate=True).values_list('name', 'grade__name', 'school__name').order_by('grade__name')
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response