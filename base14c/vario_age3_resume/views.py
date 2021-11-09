from django.shortcuts import render, redirect
from .forms import Vario_Age3_ResumeForm
from .models import Vario_Age3_Resume
from .filters import Vario_Age3_ResumeFiltre
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
def list_vario_age3_resume(request):
    vario_age3_resumes = Vario_Age3_Resume.objects.all().order_by('-id')
    myFilter = Vario_Age3_ResumeFiltre(request.GET, queryset=vario_age3_resumes)
    vario_age3_resumes = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vario_age3_resume.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('vario_age3_resume')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Vario_Age3_Resume._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = vario_age3_resumes.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'vario_age3_resumes': vario_age3_resumes, 'myFilter': myFilter}
    return render(request, 'vario_age3_resume/vario_age3_resume.html', context)


@login_required(login_url='login')
def ajouter_vario_age3_resume(request):
    form = Vario_Age3_ResumeForm()
    if request.method == 'POST':
        form = Vario_Age3_ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vario_age3_resume/')
    context = {'form': form}
    return render(request, 'vario_age3_resume/ajout_vario_age3_resume.html', context)


@login_required(login_url='login')
def modifier_vario_age3_resume(request, pk):
    key = Vario_Age3_Resume.objects.get(id=pk)
    form = Vario_Age3_ResumeForm(instance=key)
    if request.method == 'POST':
        form = Vario_Age3_ResumeForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/vario_age3_resume')
    context = {'form': form}
    return render(request, 'vario_age3_resume/ajout_vario_age3_resume.html', context)


def supprimer_vario_age3_resume(request, pk):
    context = {}
    obj = Vario_Age3_Resume.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/vario_age3_resume')
    return render(request, 'vario_age3_resume/ajout_vario_age3_resume.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadvario_age3_resume(request):
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
                    obj = Vario_Age3_Resume(
                        measurement_name=sheet.cell_value(rowx=i, colx=0),
                        tin_capsule_lot=sheet.cell_value(rowx=i, colx=1),
                        expected_weight=sheet.cell_value(rowx=i, colx=2),
                        weighing_operator=sheet.cell_value(rowx=i, colx=3),
                        weighing_date=(sheet.cell_value(rowx=i, colx=4)) if (
                                    sheet.cell_value(rowx=i, colx=4) != "") else None,
                        weight=sheet.cell_value(rowx=i, colx=5),
                        Vario_measurement_name=sheet.cell_value(rowx=i, colx=6),
                        humidity=sheet.cell_value(rowx=i, colx=7) if (
                                    sheet.cell_value(rowx=i, colx=7) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=7), float)) else None,
                        N_area=sheet.cell_value(rowx=i, colx=8) if (
                                    sheet.cell_value(rowx=i, colx=8) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=8), float)) else None,
                        C_area=sheet.cell_value(rowx=i, colx=9) if (
                                    sheet.cell_value(rowx=i, colx=9) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=9), float)) else None,
                        n_percent=sheet.cell_value(rowx=i, colx=10) if (
                                    sheet.cell_value(rowx=i, colx=10) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=10), float)) else None,
                        c_percent=sheet.cell_value(rowx=i, colx=11) if (
                                    sheet.cell_value(rowx=i, colx=11) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=11), float)) else None,
                        C_N_ratio=sheet.cell_value(rowx=i, colx=12) if (
                                    sheet.cell_value(rowx=i, colx=12) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=12), float)) else None,
                        method=sheet.cell_value(rowx=i, colx=13),
                        N_factor=sheet.cell_value(rowx=i, colx=14) if (
                                    sheet.cell_value(rowx=i, colx=14) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=14), float)) else None,
                        C_factor=sheet.cell_value(rowx=i, colx=15) if (
                                    sheet.cell_value(rowx=i, colx=15) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=15), float)) else None,
                        N_blk=sheet.cell_value(rowx=i, colx=16) if (
                                    sheet.cell_value(rowx=i, colx=16) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=16), float)) else None,
                        C_blk=sheet.cell_value(rowx=i, colx=17) if (
                                    sheet.cell_value(rowx=i, colx=17) != "" and isinstance(
                                sheet.cell_value(rowx=i, colx=17), float)) else None,
                        Memo=sheet.cell_value(rowx=i, colx=18),
                        info=sheet.cell_value(rowx=i, colx=19),
                        graphitisation_date=(sheet.cell_value(rowx=i, colx=20)) if (
                                    sheet.cell_value(rowx=i, colx=20) != "") else None,
                        comment=sheet.cell_value(rowx=i, colx=21),
                        age_nr=sheet.cell_value(rowx=i, colx=22),
                    )
                    obj.save()
                    j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/vario_age3_resume/')
    else:
        form = UploadFileForm()
    return render(request, 'vario_age3_resume/upload_vario_age3_resume.html', {'form': form})
