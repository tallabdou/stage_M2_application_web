from django.shortcuts import render, redirect
from .forms import GG_ResumeForm
from .models import GG_Resume
from .filters import GG_ResumeFiltre
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required
from django import forms
import os
import tempfile
import xlrd
from gg_sequence_resume.models import GG_Sequence_Resume
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def list_gg_resume(request):
    gg_resumes = GG_Resume.objects.all().order_by('-id')
    myFilter = GG_ResumeFiltre(request.GET, queryset=gg_resumes)
    gg_resumes = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="gg_resume.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('gg_resume')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in GG_Resume._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = gg_resumes.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'gg_resumes': gg_resumes, 'myFilter': myFilter}
    return render(request, 'gg_resume/gg_resume.html', context)


@login_required(login_url='login')
def ajouter_gg_resume(request):
    form = GG_ResumeForm()
    if request.method == 'POST':
        form = GG_ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gg_resume/')
    context = {'form': form}
    return render(request, 'gg_resume/ajout_gg_resume.html', context)


@login_required(login_url='login')
def modifier_gg_resume(request, pk):
    key = GG_Resume.objects.get(id=pk)
    form = GG_ResumeForm(instance=key)
    if request.method == 'POST':
        form = GG_ResumeForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/gg_resume')
    context = {'form': form}
    return render(request, 'gg_resume/ajout_gg_resume.html', context)


def supprimer_gg_resume(request, pk):
    context = {}
    obj = GG_Resume.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/gg_resume')
    return render(request, 'gg_resume/ajout_gg_resume.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadgg_resume(request):
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
                    if not GG_Sequence_Resume.objects.filter(GG_nr=sheet.cell_value(rowx=i, colx=0)).exists():
                        messages.error(request,
                                       "GG nr line " + str(i + 1) + " does not exist in sample GG sequence resume")
                        break
                    else:
                        obj = GG_Resume(
                            GG_nr=GG_Sequence_Resume.objects.get(GG_nr=sheet.cell_value(rowx=i, colx=0)) if (
                                        sheet.cell_value(rowx=i, colx=0) != "" and GG_Sequence_Resume.objects.filter(
                                    GG_nr=sheet.cell_value(rowx=i, colx=0)).exists()) else None,
                            GifA_nr_GG=sheet.cell_value(rowx=i, colx=1),
                            graphitisation_Date=(sheet.cell_value(rowx=i, colx=2)) if (
                                        sheet.cell_value(rowx=i, colx=2) != "") else None,
                            Operator=sheet.cell_value(rowx=i, colx=3),
                            CO2_line=sheet.cell_value(rowx=i, colx=4),
                            P_CO2=sheet.cell_value(rowx=i, colx=5),
                            weigh_mgC=sheet.cell_value(rowx=i, colx=6) if (
                                        sheet.cell_value(rowx=i, colx=6) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=6), float)) else None,
                            Measured_P_CO2=int(sheet.cell_value(rowx=i, colx=7)) if (
                                        sheet.cell_value(rowx=i, colx=7) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=7), float)) else None,
                            graphitisation_beginning_P=(sheet.cell_value(rowx=i, colx=8)) if (
                                        sheet.cell_value(rowx=i, colx=8) != "") else None,
                            expected_Pfin=int(sheet.cell_value(rowx=i, colx=9)) if (
                                        sheet.cell_value(rowx=i, colx=9) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=9), float)) else None,
                            Measured_Pfin=(sheet.cell_value(rowx=i, colx=10)) if (
                                        sheet.cell_value(rowx=i, colx=10) != "") else None,
                            beginning_hour=(sheet.cell_value(rowx=i, colx=11)) if (
                                        sheet.cell_value(rowx=i, colx=11) != "") else None,
                            ending_hour=(sheet.cell_value(rowx=i, colx=12)) if (
                                        sheet.cell_value(rowx=i, colx=12) != "") else None,
                            line_nr=sheet.cell_value(rowx=i, colx=13),
                            comment=sheet.cell_value(rowx=i, colx=14),
                            iron_mg=sheet.cell_value(rowx=i, colx=15),
                            weighing_operator=sheet.cell_value(rowx=i, colx=16),
                            comment_weighing_operator=sheet.cell_value(rowx=i, colx=17),
                            press_date=(sheet.cell_value(rowx=i, colx=18)) if (
                                        sheet.cell_value(rowx=i, colx=18) != "") else None,
                            press_operator=sheet.cell_value(rowx=i, colx=19),
                            comment_operator=sheet.cell_value(rowx=i, colx=20),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/gg_resume/')
    else:
        form = UploadFileForm()
    return render(request, 'gg_resume/upload_gg_resume.html', {'form': form})
