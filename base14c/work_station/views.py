from django.shortcuts import render, redirect
from .models import Work_Station
from .forms import Work_StationForm
from .filters import Work_StationFiltre
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required
from django import forms
import os
import tempfile
import xlrd
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def list_work_station(request):
    work_stations = Work_Station.objects.all()
    myFilter = Work_StationFiltre(request.GET, queryset=work_stations)
    work_stations = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="work_station.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('work_station')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Work_Station._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = work_stations.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'work_stations': work_stations, 'myFilter': myFilter}
    return render(request, 'work_station/work_station.html', context)


@login_required(login_url='login')
def ajouter_work_station(request):
    form = Work_StationForm()
    if request.method == 'POST':
        form = Work_StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/work_station/')
    context = {'form': form}
    return render(request, 'work_station/ajout_work_station.html', context)


@login_required(login_url='login')
def modifier_work_station(request, pk):
    key = Work_Station.objects.get(work_bench_ID=pk)
    form = Work_StationForm(instance=key)
    if request.method == 'POST':
        form = Work_StationForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/work_station')
    context = {'form': form}
    return render(request, 'work_station/ajout_work_station.html', context)


def supprimer_work_station(request, pk):
    context = {}
    obj = Work_Station.objects.get(work_bench_ID=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/work_station')
    return render(request, 'work_station/ajout_work_station.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadwork_station(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            fd, path = tempfile.mkstemp()  # mkstemp returns a tuple: an integer (index) called file descriptor used by OS to refer to a file and its path
            try:
                with os.fdopen(fd, 'wb') as tmp:
                    tmp.write(excel_file.read())
                book = xlrd.open_workbook(path)
                sheet = book.sheet_by_index(0)
                j = 0
                for i in range(1, sheet.nrows):
                    if Work_Station.objects.filter(work_bench_ID=sheet.cell_value(rowx=i, colx=0)).exists():
                        messages.error(request, "Work bench ID line " + str(i + 1) + " already exists")
                        break
                    elif not isinstance(sheet.cell_value(rowx=i, colx=0), float):
                        messages.error(request, "Work bench ID line " + str(i + 1) + " is not valid")
                        break
                    else:
                        obj = Work_Station(
                            work_bench_ID=int(sheet.cell_value(rowx=i, colx=0)),
                            work_bench_description=sheet.cell_value(rowx=i, colx=1),
                            localisation=sheet.cell_value(rowx=i, colx=2),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/work_station/')
    else:
        form = UploadFileForm()
    return render(request, 'work_station/upload_work_station.html', {'form': form})
