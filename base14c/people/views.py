from django.shortcuts import render, redirect
from .models import People
from .forms import PeopleForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
import os
import tempfile
import xlrd
from .filters import PeopleFiltre
from django.http import HttpResponse
import xlwt


def list_people(request):
    peoples = People.objects.all().order_by('name')
    myFilter = PeopleFiltre(request.GET, queryset=peoples)
    peoples = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="people.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('people')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [f.name for f in People._meta.concrete_fields]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = peoples.values_list()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'peoples': peoples, 'myFilter': myFilter}
    return render(request, 'people/people.html', context)


@login_required(login_url='login')
def ajouter_people(request):
    form = PeopleForm()
    if request.method == 'POST':
        form = PeopleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/people')
    context = {'form': form}
    return render(request, 'people/ajout_people.html', context)


@login_required(login_url='login')
def modifier_people(request, pk):
    key = People.objects.get(id=pk)
    form = PeopleForm(instance=key)
    if request.method == 'POST':
        form = PeopleForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/people')
    context = {'form': form}
    return render(request, 'people/ajout_people.html', context)


def supprimer_people(request, pk):
    context = {}
    obj = People.objects.get(GifA=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/people')
    return render(request, 'people/ajout_people.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadpeople(request):
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
                    if sheet.cell_value(rowx=i, colx=0) == "":
                        messages.error(request, "Name line " + str(i + 1) + " is null")
                        break
                    else:
                        obj = People(
                            name=sheet.cell_value(rowx=i, colx=0),
                            first_name=sheet.cell_value(rowx=i, colx=1),
                            affiliation=sheet.cell_value(rowx=i, colx=2),
                            address=sheet.cell_value(rowx=i, colx=3),
                            email=sheet.cell_value(rowx=i, colx=4),
                            phone_number=sheet.cell_value(rowx=i, colx=5),
                            lsce_contact=int(sheet.cell_value(rowx=i, colx=6)) if (
                                        sheet.cell_value(rowx=i, colx=6) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=6), float)) else 0,
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/sample/')
    else:
        form = UploadFileForm()
    return render(request, 'sample/upload_sample.html', {'form': form})
