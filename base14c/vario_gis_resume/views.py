from django.shortcuts import render, redirect
from .models import Vario_Gis_Resume
from .forms import Vario_Gis_ResumeForm
from .filters import Vario_Gis_ResumeFiltre
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
def list_vario_gis_resume(request):
    vario_gis_resumes = Vario_Gis_Resume.objects.all().order_by('-id')
    myFilter = Vario_Gis_ResumeFiltre(request.GET, queryset=vario_gis_resumes)
    vario_gis_resumes = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vario_gis_resume.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('vario_gis_resume')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Vario_Gis_Resume._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = vario_gis_resumes.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'vario_gis_resumes': vario_gis_resumes, 'myFilter': myFilter}
    return render(request, 'vario_gis_resume/vario_gis_resume.html', context)

@login_required(login_url='login')
def ajouter_vario_gis_resume(request):
    form = Vario_Gis_ResumeForm()
    if request.method == 'POST':
        form = Vario_Gis_ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vario_gis_resume/')
    context = {'form': form}
    return render(request, 'vario_gis_resume/ajout_vario_gis_resume.html', context)



@login_required(login_url='login')
def modifier_vario_gis_resume(request, pk):
    key = Vario_Gis_Resume.objects.get(id=pk)
    form = Vario_Gis_ResumeForm(instance=key)
    if request.method == 'POST':
        form = Vario_Gis_ResumeForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/vario_gis_resume')
    context = {'form': form}
    return render(request, 'vario_gis_resume/ajout_vario_gis_resume.html', context)

def supprimer_vario_gis_resume(request, pk):
    context = {}
    obj = Vario_Gis_Resume.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/vario_gis_resume')
    return render(request, 'vario_gis_resume/ajout_vario_gis_resume.html', context)



class UploadFileForm(forms.Form):
    file = forms.FileField()

def uploadvario_gis_resume(request):
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
                    obj=Vario_Gis_Resume(
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
                        vario_gis_date=(sheet.cell_value(rowx=i, colx=20)) if (
                                    sheet.cell_value(rowx=i, colx=20) != "") else None,
                        comment=sheet.cell_value(rowx=i, colx=21),
                        )
                    obj.save()
                    j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/vario_gis_resume/')
    else:
        form = UploadFileForm()
    return render(request,'vario_gis_resume/upload_vario_gis_resume.html', {'form':form})