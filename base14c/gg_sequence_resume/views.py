from django.shortcuts import render, redirect
from .forms import GG_Sequence_ResumeForm
from .models import GG_Sequence_Resume
from .filters import GG_Sequence_ResumeFiltre
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
def list_gg_sequence_resume(request):
    gg_sequence_resumes = GG_Sequence_Resume.objects.all()
    myFilter = GG_Sequence_ResumeFiltre(request.GET, queryset=gg_sequence_resumes)
    gg_sequence_resumes = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="gg_sequence_resume.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('gg_sequence_resume')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in GG_Sequence_Resume._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = gg_sequence_resumes.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'gg_sequence_resumes': gg_sequence_resumes, 'myFilter': myFilter}
    return render(request, 'gg_sequence_resume/gg_sequence_resume.html', context)


@login_required(login_url='login')
def ajouter_gg_sequence_resume(request):
    form = GG_Sequence_ResumeForm()
    if request.method == 'POST':
        form = GG_Sequence_ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gg_sequence_resume/')
    context = {'form': form}
    return render(request, 'gg_sequence_resume/ajout_gg_sequence_resume.html', context)


@login_required(login_url='login')
def modifier_gg_sequence_resume(request, pk):
    key = GG_Sequence_Resume.objects.get(GG_nr=pk)
    form = GG_Sequence_ResumeForm(instance=key)
    if request.method == 'POST':
        form = GG_Sequence_ResumeForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/gg_sequence_resume')
    context = {'form': form}
    return render(request, 'gg_sequence_resume/ajout_gg_sequence_resume.html', context)


def supprimer_gg_sequence_resume(request, pk):
    context = {}
    obj = GG_Sequence_Resume.objects.get(GG_nr=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/gg_sequence_resume')
    return render(request, 'gg_sequence_resume/ajout_gg_sequence_resume.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadgg_sequence_resume(request):
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
                        messages.error(request, "GG nr line" + str(i + 1) + " is null")
                        break
                    else:
                        obj = GG_Sequence_Resume(
                            GG_nr=(sheet.cell_value(rowx=i, colx=0)),
                            graph=sheet.cell_value(rowx=i, colx=1),
                            comment=sheet.cell_value(rowx=i, colx=2),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/gg_sequence_resume/')
    else:
        form = UploadFileForm()
    return render(request, 'gg_sequence_resume/upload_gg_sequence_resume.html', {'form': form})
