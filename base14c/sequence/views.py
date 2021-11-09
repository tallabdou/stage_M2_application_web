from django.shortcuts import render, redirect
from .forms import SequenceForm
from .models import Sequence
from .filters import SequenceFiltre
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
def list_sequence(request):
    sequences = Sequence.objects.all()
    myFilter = SequenceFiltre(request.GET, queryset=sequences)
    sequences = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sequence.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sequence')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Sequence._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = sequences.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'sequences': sequences, 'myFilter': myFilter}
    return render(request, 'sequence/sequence.html', context)


@login_required(login_url='login')
def ajouter_sequence(request):
    form = SequenceForm()
    if request.method == 'POST':
        form = SequenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/sequence/')
    context = {'form': form}
    return render(request, 'sequence/ajout_sequence.html', context)


@login_required(login_url='login')
def modifier_sequence(request, pk):
    key = Sequence.objects.get(sequence_ID=pk)
    form = SequenceForm(instance=key)
    if request.method == 'POST':
        form = SequenceForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/sequence')
    context = {'form': form}
    return render(request, 'sequence/ajout_sequence.html', context)


def supprimer_sequence(request, pk):
    context = {}
    obj = Sequence.objects.get(sequence_ID=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/sequence')
    return render(request, 'sequence/ajout_sequence.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadsequence(request):
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
                        messages.error(request, "Sequence ID line " + str(i + 1) + " is null")
                        break
                    elif Sequence.objects.filter(sequence_ID=sheet.cell_value(rowx=i, colx=0)).exists():
                        messages.error(request, "Sequence ID line " + str(i + 1) + " already exists")
                        break
                    else:
                        obj = Sequence(
                            sequence_ID=sheet.cell_value(rowx=i, colx=0),
                            sequence_name=sheet.cell_value(rowx=i, colx=1),
                            description=sheet.cell_value(rowx=i, colx=2),
                            comment=sheet.cell_value(rowx=i, colx=3),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/sequence/')
    else:
        form = UploadFileForm()
    return render(request, 'sequence/upload_sequence.html', {'form': form})
