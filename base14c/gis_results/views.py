from django.shortcuts import render, redirect
from .forms import Gis_ResultsForm
from .models import Gis_Results
from .filters import Gis_ResultsFiltre
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
def list_gis_results(request):
    gis_resultss = Gis_Results.objects.all().order_by('-Echo')
    myFilter = Gis_ResultsFiltre(request.GET, queryset=gis_resultss)
    gis_resultss = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="gis_results.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('gis_results')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [f.name for f in Gis_Results._meta.get_fields()]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = gis_resultss.values_list()
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'gis_resultss': gis_resultss, 'myFilter': myFilter}
    return render(request, 'gis_results/gis_results.html', context)


@login_required(login_url='login')
def ajouter_gis_results(request):
    form = Gis_ResultsForm()
    if request.method == 'POST':
        form = Gis_ResultsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gis_results/')
    context = {'form': form}
    return render(request, 'gis_results/ajout_gis_results.html', context)


@login_required(login_url='login')
def modifier_gis_results(request, pk):
    key = Gis_Results.objects.get(Echo=pk)
    form = Gis_ResultsForm(instance=key)
    if request.method == 'POST':
        form = Gis_ResultsForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/gis_results')
    context = {'form': form}
    return render(request, 'gis_results/ajout_gis_results.html', context)


def supprimer_gis_results(request, pk):
    context = {}
    obj = Gis_Results.objects.get(Echo=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/gis_results')
    return render(request, 'gis_results/ajout_gis_results.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadgis_results(request):
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
                    if sheet.cell_value(rowx=i, colx=0) == "" or not (
                    isinstance(sheet.cell_value(rowx=i, colx=0), float)):
                        messages.error(request, "Echo n° line " + str(i + 1) + " is invalid")
                        break
                    else:
                        obj = Gis_Results(
                            Echo=int(sheet.cell_value(rowx=i, colx=0)),
                            GifA_nr=sheet.cell_value(rowx=i, colx=1),
                            target_comment=sheet.cell_value(rowx=i, colx=2),
                            ratio_14_12=sheet.cell_value(rowx=i, colx=3),
                            erreur_ratio=sheet.cell_value(rowx=i, colx=4),
                            F14C=sheet.cell_value(rowx=i, colx=5),
                            erreur_F14C=sheet.cell_value(rowx=i, colx=6) if (
                                        sheet.cell_value(rowx=i, colx=6) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=6), float)) else None,
                            C14_Age=(sheet.cell_value(rowx=i, colx=7)) if (
                                        sheet.cell_value(rowx=i, colx=7) != "") else None,
                            age_uncertainty=sheet.cell_value(rowx=i, colx=8),
                            current_12C=sheet.cell_value(rowx=i, colx=9),
                            weight_ug_C=sheet.cell_value(rowx=i, colx=10),
                            integration_time=sheet.cell_value(rowx=i, colx=11),
                            std_corr=sheet.cell_value(rowx=i, colx=12),
                            blc_corr_F14C=sheet.cell_value(rowx=i, colx=13),
                            const_cont_masse=sheet.cell_value(rowx=i, colx=14),
                            const_cont_ratio=sheet.cell_value(rowx=i, colx=15),
                            cross_cont=sheet.cell_value(rowx=i, colx=16),
                            d13c=sheet.cell_value(rowx=i, colx=17),

                            GIS_label=sheet.cell_value(rowx=i, colx=18),
                            expected_weight=sheet.cell_value(rowx=i, colx=19),
                            method=sheet.cell_value(rowx=i, colx=20),
                            sample_name=sheet.cell_value(rowx=i, colx=21),
                            smp_position=sheet.cell_value(rowx=i, colx=22),
                            ugC_measured_bis=sheet.cell_value(rowx=i, colx=23),
                            ugC_kept_bis=sheet.cell_value(rowx=i, colx=24),
                            weighted_sample=sheet.cell_value(rowx=i, colx=25),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/gis_results/')
    else:
        form = UploadFileForm()
    return render(request, 'gis_results/upload_gis_results.html', {'form': form})
