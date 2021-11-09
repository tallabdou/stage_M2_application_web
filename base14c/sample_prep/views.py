from django.shortcuts import render, redirect
from .forms import SamplePrepForm, SamplePrepForm2
from .models import Sample_Prep
from .filters import SamplePrepFiltre
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required
from django import forms
import os
import tempfile
import xlrd
from sequence.models import Sequence
from django.contrib import messages
from sample.models import Sample


# Create your views here.
@login_required(login_url='login')
def list_sample_prep(request):
    samples_prep = Sample_Prep.objects.all().order_by('-id')
    myFilter = SamplePrepFiltre(request.GET, queryset=samples_prep)
    samples_prep = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sample_prep.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sample_prep')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Sample_Prep._meta.get_fields()]
        # columns = [f.name for f in Sample_Prep._meta.get_fields() if f.name != 'id']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = samples_prep.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'samples_prep': samples_prep, 'myFilter': myFilter}
    return render(request, 'sample_prep/sample_prep.html', context)


@login_required(login_url='login')
def ajouter_sample_prep(request):
    form = SamplePrepForm()
    if request.method == 'POST':
        form = SamplePrepForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            GifA_prep_test = "GifA" + str(instance.sample) + str(instance.preparation_declination)
            if not Sample_Prep.objects.filter(GifA_prep=GifA_prep_test).exists():
                instance = form.save()
                input = Sample_Prep.objects.get(id=instance.id)
                input.GifA_prep = "GifA" + str(input.sample) + str(input.preparation_declination)
                input.save()
                return redirect('/sample_prep/')
            elif form.is_valid() and Sample_Prep.objects.filter(GifA_prep=GifA_prep_test).exists():
                messages.success(request, 'GifA already exists')
                form = SamplePrepForm(request.POST)
    context = {'form': form}
    return render(request, 'sample_prep/ajout_sample_prep.html', context)


@login_required(login_url='login')
def modifier_sample_prep(request, pk):
    key = Sample_Prep.objects.get(id=pk)
    form = SamplePrepForm(instance=key)
    if request.method == 'POST':
        form = SamplePrepForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/sample_prep')
    context = {'form': form}
    return render(request, 'sample_prep/ajout_sample_prep.html', context)


def supprimer_sample_prep(request, pk):
    context = {}
    obj = Sample_Prep.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/sample_prep')
    return render(request, 'sample_prep/ajout_sample_prep.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadsample_prep(request):
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
                    if Sample_Prep.objects.filter(GifA_prep=sheet.cell_value(rowx=i, colx=2)).exists():
                        messages.error(request, "GifA line " + str(i + 1) + " already exists")
                        break
                    elif not Sample.objects.filter(GifA=int(sheet.cell_value(rowx=i, colx=0))).exists():
                        messages.error(request, "Line " + str(i + 1) + " : GifA number does not exist in sample table")
                        break
                    else:
                        obj = Sample_Prep(
                            sample=Sample.objects.get(GifA=int(sheet.cell_value(rowx=i, colx=0))) if (
                                        sheet.cell_value(rowx=i, colx=0) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=0), float) and Sample.objects.filter(
                                    GifA=int(sheet.cell_value(rowx=i, colx=0))).exists()) else None,
                            preparation_declination=sheet.cell_value(rowx=i, colx=1),
                            GifA_prep=sheet.cell_value(rowx=i, colx=2),
                            sequence=Sequence.objects.get(sequence_ID=sheet.cell_value(rowx=i, colx=3)) if (
                                        sheet.cell_value(rowx=i, colx=3) != "" and Sequence.objects.filter(
                                    sequence_ID=sheet.cell_value(rowx=i, colx=3)).exists()) else None,
                            prep_warning=sheet.cell_value(rowx=i, colx=4),
                            comment=sheet.cell_value(rowx=i, colx=5),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/sample_prep/')
    else:
        form = UploadFileForm()
    return render(request, 'sample_prep/upload_sample_prep.html', {'form': form})


@login_required(login_url='login')
def last_sample_prep(request):
    form2 = SamplePrepForm2()
    if request.method == 'POST':
        form2 = SamplePrepForm2(request.POST)
        instance = form2.save(commit=False)
        form2 = SamplePrepForm2()
        last = Sample_Prep.objects.filter(sample=instance.sample).latest('id').preparation_declination
        form2.fields['sample'].initial = instance.sample
        form2.fields['preparation_declination'].initial = last
    context = {'form2': form2}
    return render(request, 'sample_prep/last_sample_prep.html', context)
