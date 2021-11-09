from django.shortcuts import render, redirect
from .forms import Age3_Sequence_ResumeForm
from .models import Age3_Sequence_Resume
from .filters import Age3_Sequence_ResumeFiltre
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
def list_age3_sequence_resume(request):
    age3_sequence_resumes = Age3_Sequence_Resume.objects.all()
    myFilter = Age3_Sequence_ResumeFiltre(request.GET, queryset=age3_sequence_resumes)
    age3_sequence_resumes = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="age3_sequence_resume.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('age3_sequence_resume')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Age3_Sequence_Resume._meta.concrete_fields if f.name != 'age3_resume']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = age3_sequence_resumes.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'age3_sequence_resumes': age3_sequence_resumes, 'myFilter': myFilter}
    return render(request, 'age3_sequence_resume/age3_sequence_resume.html', context)


@login_required(login_url='login')
def ajouter_age3_sequence_resume(request):
    form = Age3_Sequence_ResumeForm()
    if request.method == 'POST':
        form = Age3_Sequence_ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/age3_sequence_resume/')
    context = {'form': form}
    return render(request, 'age3_sequence_resume/ajout_age3_sequence_resume.html', context)


@login_required(login_url='login')
def modifier_age3_sequence_resume(request, pk):
    key = Age3_Sequence_Resume.objects.get(age_nr=pk)
    form = Age3_Sequence_ResumeForm(instance=key)
    if request.method == 'POST':
        form = Age3_Sequence_ResumeForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/age3_sequence_resume')
    context = {'form': form}
    return render(request, 'age3_sequence_resume/ajout_age3_sequence_resume.html', context)


def supprimer_age3_sequence_resume(request, pk):
    context = {}
    obj = Age3_Sequence_Resume.objects.get(age_nr=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/age3_sequence_resume')
    return render(request, 'age3_sequence_resume/ajout_age3_sequence_resume.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadage3_sequence_resume(request):
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
                    if Age3_Sequence_Resume.objects.filter(age_nr=sheet.cell_value(rowx=i, colx=0)).exists():
                        messages.error(request, "Age nr line " + str(i + 1) + " already exists")
                        break
                    else:
                        obj = Age3_Sequence_Resume(
                            age_nr=sheet.cell_value(rowx=i, colx=0),
                            age_graph=sheet.cell_value(rowx=i, colx=1),
                            operator=sheet.cell_value(rowx=i, colx=2),
                            comment=sheet.cell_value(rowx=i, colx=3),
                            maintenance_date=(sheet.cell_value(rowx=i, colx=4)) if (
                                        sheet.cell_value(rowx=i, colx=4) != "") else None,
                            operator_maintenance=sheet.cell_value(rowx=i, colx=5),
                            ash=int(sheet.cell_value(rowx=i, colx=6)) if (
                                        sheet.cell_value(rowx=i, colx=6) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=6), float)) else None,
                            combustion_colomn=int(sheet.cell_value(rowx=i, colx=7)) if (
                                        sheet.cell_value(rowx=i, colx=7) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=7), float)) else None,
                            regenerated_copper_reduction_colomn=int(sheet.cell_value(rowx=i, colx=8)) if (
                                        sheet.cell_value(rowx=i, colx=8) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=8), float)) else None,
                            new_copper_reduction_colomn=int(sheet.cell_value(rowx=i, colx=9)) if (
                                        sheet.cell_value(rowx=i, colx=9) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=9), float)) else None,
                            sicapent=sheet.cell_value(rowx=i, colx=10),
                            ball_valve=sheet.cell_value(rowx=i, colx=11) if (
                                        sheet.cell_value(rowx=i, colx=11) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=11), float)) else None,
                            comments=sheet.cell_value(rowx=i, colx=12),
                            O2_pressure=sheet.cell_value(rowx=i, colx=13),
                            He_pressure=sheet.cell_value(rowx=i, colx=14),
                            H2_pressure=sheet.cell_value(rowx=i, colx=15),
                            Ar_pressure=sheet.cell_value(rowx=i, colx=16),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/age3_sequence_resume/')
    else:
        form = UploadFileForm()
    return render(request, 'age3_sequence_resume/upload_age3_sequence_resume.html', {'form': form})
