from django.shortcuts import render, redirect
from .forms import Prep_StepForm
from .models import Prep_Step
from .filters import Prep_StepFiltre
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required
from django import forms
import os
import tempfile
import xlrd
from sequence.models import Sequence
from django.contrib import messages
from people.models import People
from work_station.models import Work_Station


# Create your views here.
@login_required(login_url='login')
def list_prep_step(request):
    prep_steps = Prep_Step.objects.all().order_by('-id')
    myFilter = Prep_StepFiltre(request.GET, queryset=prep_steps)
    prep_steps = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="prep_step.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('prep_step')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Prep_Step._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = prep_steps.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'prep_steps': prep_steps, 'myFilter': myFilter}
    return render(request, 'prep_step/prep_step.html', context)

@login_required(login_url='login')
def ajouter_prep_step(request):
    form = Prep_StepForm()
    if request.method == 'POST':
        form = Prep_StepForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/prep_step/')
    context = {'form': form}
    return render(request, 'prep_step/ajout_prep_step.html', context)


@login_required(login_url='login')
def modifier_prep_step(request, pk):
    key = Prep_Step.objects.get(id=pk)
    form = Prep_StepForm(instance=key)
    if request.method == 'POST':
        form = Prep_StepForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/prep_step')
    context = {'form': form}
    return render(request, 'prep_step/ajout_prep_step.html', context)

def supprimer_prep_step(request, pk):
    context = {}
    obj = Prep_Step.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/prep_step')
    return render(request, 'prep_step/ajout_prep_step.html', context)



class UploadFileForm(forms.Form):
    file = forms.FileField()

def uploadprep_step(request):
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
                j=0
                for i in range(1,sheet.nrows):
                    obj=Prep_Step(
                        work_station=Work_Station.objects.get(work_bench_ID=int(sheet.cell_value(rowx=i, colx=0))) if (sheet.cell_value(rowx=i, colx=0)!="" and isinstance(sheet.cell_value(rowx=i, colx=0),float) and Work_Station.objects.filter(work_bench_ID=int(sheet.cell_value(rowx=i, colx=0))).exists() ) else None,
                        sequence= Sequence.objects.get(sequence_ID=sheet.cell_value(rowx=i, colx=1)) if (sheet.cell_value(rowx=i, colx=1)!="" and Sequence.objects.filter(sequence_ID=int(sheet.cell_value(rowx=i, colx=1))).exists() ) else None,
                        operator=People.objects.get(id=sheet.cell_value(rowx=i, colx=2)) if (sheet.cell_value(rowx=i, colx=2)!="" and People.objects.filter(id=int(sheet.cell_value(rowx=i, colx=2))).exists() ) else None,
                        ending_date= sheet.cell_value(rowx=i, colx=3) if (sheet.cell_value(rowx=i, colx=3)!= "") else None,
                        )
                    obj.save()
                    j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/prep_step/')
    else:
        form = UploadFileForm()
    return render(request,'prep_step/upload_prep_step.html', {'form':form})