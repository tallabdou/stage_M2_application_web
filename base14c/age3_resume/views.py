from django.shortcuts import render, redirect
from .forms import Age3_ResumeForm
from .models import Age3_Resume
from .filters import Age3_ResumeFiltre
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required
from age3_sequence_resume.models import Age3_Sequence_Resume


# Create your views here.
@login_required(login_url='login')
def list_age3_resume(request):
    age3_resumes = Age3_Resume.objects.all()
    myFilter = Age3_ResumeFiltre(request.GET, queryset=age3_resumes)
    age3_resumes = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="age3_resume.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('age3_resume')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [f.name for f in Age3_Resume._meta.concrete_fields]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = age3_resumes.values_list()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'age3_resumes': age3_resumes, 'myFilter': myFilter}
    return render(request, 'age3_resume/age3_resume.html', context)


from django.contrib import messages


@login_required(login_url='login')
def ajouter_age3_resume(request):
    form = Age3_ResumeForm()
    if request.method == 'POST':
        form = Age3_ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/age3_resume/')
    context = {'form': form}
    return render(request, 'age3_resume/ajout_age3_resume.html', context)


@login_required(login_url='login')
def modifier_age3_resume(request, pk):
    key = Age3_Resume.objects.get(id=pk)
    form = Age3_ResumeForm(instance=key)
    if request.method == 'POST':
        form = Age3_ResumeForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/age3_resume')
    context = {'form': form}
    return render(request, 'age3_resume/ajout_age3_resume.html', context)


def supprimer_age3_resume(request, pk):
    context = {}
    obj = Age3_Resume.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/age3_resume')
    return render(request, 'age3_resume/ajout_age3_resume.html', context)


from django import forms
from django.contrib import messages

import os
import tempfile
import xlrd


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadage3_resume(request):
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
                    obj = Age3_Resume(
                        GifA_nr_age3=sheet.cell_value(rowx=i, colx=0),
                        total_sample_weight=sheet.cell_value(rowx=i, colx=1) if (
                                    sheet.cell_value(rowx=i, colx=1) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=1), float)) else None,
                        CO2_ug=int(sheet.cell_value(rowx=i, colx=2)) if (
                                    sheet.cell_value(rowx=i, colx=2) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=2), float)) else None,
                        CO2fin_ug=int(sheet.cell_value(rowx=i, colx=3)) if (
                                    sheet.cell_value(rowx=i, colx=3) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=3), float)) else None,
                        COH2_mbar=int(sheet.cell_value(rowx=i, colx=4)) if (
                                    sheet.cell_value(rowx=i, colx=4) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=4), float)) else None,
                        Time_min=int(sheet.cell_value(rowx=i, colx=5)) if (
                                    sheet.cell_value(rowx=i, colx=5) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=5), float)) else None,
                        C_percent=sheet.cell_value(rowx=i, colx=6) if (
                                    sheet.cell_value(rowx=i, colx=6) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=6), float)) else None,
                        T_celsius=int(sheet.cell_value(rowx=i, colx=7)) if (
                                    sheet.cell_value(rowx=i, colx=7) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=7), float)) else None,
                        Tset_celsius=int(sheet.cell_value(rowx=i, colx=8)) if (
                                    sheet.cell_value(rowx=i, colx=8) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=8), float)) else None,
                        p_end_mbar=int(sheet.cell_value(rowx=i, colx=9)) if (
                                    sheet.cell_value(rowx=i, colx=9) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=9), float)) else None,
                        Sample_date_age3=(sheet.cell_value(rowx=i, colx=10)) if (
                                    sheet.cell_value(rowx=i, colx=10) != "") else None,
                        N_percent=sheet.cell_value(rowx=i, colx=11) if (
                                    sheet.cell_value(rowx=i, colx=11) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=11), float)) else None,
                        age_nr=Age3_Sequence_Resume.objects.get(age_nr=sheet.cell_value(rowx=i, colx=12)) if (
                                    sheet.cell_value(rowx=i, colx=12) != "" and Age3_Sequence_Resume.objects.filter(
                                age_nr=sheet.cell_value(rowx=i, colx=12)).exists()) else None,
                        reactor=int(sheet.cell_value(rowx=i, colx=13)) if (
                                    sheet.cell_value(rowx=i, colx=13) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=13), float)) else None,
                        tin_capsule_nr=int(sheet.cell_value(rowx=i, colx=14)) if (
                                    sheet.cell_value(rowx=i, colx=14) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=14), float)) else None,
                        pre_or_not=int(sheet.cell_value(rowx=i, colx=15)) if (
                                    sheet.cell_value(rowx=i, colx=15) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=15), float) and (
                                                int(sheet.cell_value(rowx=i, colx=15)) == 0 or 1)) else None,
                        graphitisation_operator=sheet.cell_value(rowx=i, colx=16),
                        graphitisation_comment=sheet.cell_value(rowx=i, colx=17),
                        iron_mg=sheet.cell_value(rowx=i, colx=18) if (
                                    sheet.cell_value(rowx=i, colx=18) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=18), float)) else None,
                        weighing_operator=sheet.cell_value(rowx=i, colx=19),
                        comment_weighing_operator=sheet.cell_value(rowx=i, colx=20),
                        press_date=(sheet.cell_value(rowx=i, colx=21)) if (
                                    sheet.cell_value(rowx=i, colx=21) != "") else None,
                        press_operator=sheet.cell_value(rowx=i, colx=22),
                        comment_press_operator=sheet.cell_value(rowx=i, colx=23),
                    )
                    obj.save()
                    j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/age3_resume/')
    else:
        form = UploadFileForm()
    return render(request, 'age3_resume/upload_age3_resume.html', {'form': form})
