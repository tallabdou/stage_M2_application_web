from django.shortcuts import render, redirect
from .forms import PaperForm
from .models import Paper
from .filters import PaperFiltre
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
def list_paper(request):
    papers = Paper.objects.all()
    myFilter = PaperFiltre(request.GET, queryset=papers)
    papers = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="paper.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('paper')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Paper._meta.get_fields() if f.name != 'sample']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = papers.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'papers': papers, 'myFilter': myFilter}
    return render(request, 'paper/paper.html', context)


@login_required(login_url='login')
def ajouter_paper(request):
    form = PaperForm()
    if request.method == 'POST':
        form = PaperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/paper/')
    context = {'form': form}
    return render(request, 'paper/ajout_paper.html', context)


@login_required(login_url='login')
def modifier_paper(request, pk):
    key = Paper.objects.get(DOI=pk)
    form = PaperForm(instance=key)
    if request.method == 'POST':
        form = PaperForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/paper')
    context = {'form': form}
    return render(request, 'paper/ajout_paper.html', context)


def supprimer_paper(request, pk):
    context = {}
    obj = Paper.objects.get(DOI=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/paper')
    return render(request, 'paper/ajout_paper.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadpaper(request):
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
                        messages.error(request, "DOI line " + str(i + 1) + " is null")
                        break
                    else:
                        obj = Paper(
                            DOI=sheet.cell_value(rowx=i, colx=0),
                            first_author=sheet.cell_value(rowx=i, colx=1),
                            year=int(sheet.cell_value(rowx=i, colx=2)) if (
                                        sheet.cell_value(rowx=i, colx=2) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=2), int)) else None,
                            title=sheet.cell_value(rowx=i, colx=3),
                            revue=sheet.cell_value(rowx=i, colx=4),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/paper/')
    else:
        form = UploadFileForm()
    return render(request, 'paper/upload_paper.html', {'form': form})
