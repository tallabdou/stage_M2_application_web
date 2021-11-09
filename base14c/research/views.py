from django.shortcuts import render, redirect
from .models import Research
from .forms import ResearchForm
from django.contrib.auth.decorators import login_required
from .filters import ResearchFiltre
from django.http import HttpResponse
import xlwt
from django import forms
import os
import tempfile
import xlrd
from django.contrib import messages
from people.models import People


# Create your views here.
@login_required(login_url='login')
def list_research(request):
    researchs = Research.objects.all().order_by('-id')
    myFilter = ResearchFiltre(request.GET, queryset=researchs)
    researchs = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="research.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('research')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Research._meta.get_fields() if f.name != 'sample']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = researchs.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'researchs': researchs, 'myFilter': myFilter}
    return render(request, 'research/research.html', context)


@login_required(login_url='login')
def ajouter_research(request):
    form = ResearchForm
    if request.method == 'POST':
        form = ResearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/research/')
    context = {'form': form}
    return render(request, 'research/ajout_research.html', context)


@login_required(login_url='login')
def modifier_research(request, pk):
    key = Research.objects.get(id=pk)
    form = ResearchForm(instance=key)
    if request.method == 'POST':
        form = ResearchForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/research')
    context = {'form': form}
    return render(request, 'research/ajout_research.html', context)


def supprimer_research(request, pk):
    context = {}
    obj = Research.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/research')
    return render(request, 'research/ajout_research.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadresearch(request):
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
                    obj = Research(
                        project_acronym=sheet.cell_value(rowx=i, colx=0),
                        project_full_name=sheet.cell_value(rowx=i, colx=1),
                        project_leader=People.objects.get(id=sheet.cell_value(rowx=i, colx=2)) if (
                                    sheet.cell_value(rowx=i, colx=2) != "" and People.objects.filter(
                                id=sheet.cell_value(rowx=i, colx=2)).exists()) else None,
                        project_co_leader=People.objects.get(id=sheet.cell_value(rowx=i, colx=3)) if (
                                    sheet.cell_value(rowx=i, colx=3) != "" and People.objects.filter(
                                id=sheet.cell_value(rowx=i, colx=3)).exists()) else None,
                        WP_leader=sheet.cell_value(rowx=i, colx=4),
                        funding_agency=sheet.cell_value(rowx=i, colx=5),
                        student_post_doc_name=sheet.cell_value(rowx=i, colx=6),
                        academic_level=sheet.cell_value(rowx=i, colx=7),
                        main_supervisor=sheet.cell_value(rowx=i, colx=8),
                        second_supervisor=sheet.cell_value(rowx=i, colx=9),
                    )
                    obj.save()
                    j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/research/')
    else:
        form = UploadFileForm()
    return render(request, 'research/upload_research.html', {'form': form})
