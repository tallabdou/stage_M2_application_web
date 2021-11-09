from django.shortcuts import render, redirect
from .forms import SampleForm
from .models import Sample
from .filters import SampleFiltre
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
import os
import tempfile
import xlrd
from people.models import People
from research.models import Research
from paper.models import Paper


# Create your views here.
@login_required(login_url='login')
def list_sample(request):
    samples = Sample.objects.all().order_by('-receipt_date')
    myFilter = SampleFiltre(request.GET, queryset=samples)
    samples = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sample.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sample')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [f.name for f in Sample._meta.concrete_fields]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = samples.values_list()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'samples': samples, 'myFilter': myFilter}
    return render(request, 'sample/sample.html', context)


@login_required(login_url='login')
def ajouter_sample(request):
    form = SampleForm()
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/sample/')
    context = {'form': form}
    return render(request, 'sample/ajout_sample.html', context)


@login_required(login_url='login')
def modifier_sample(request, pk):
    key = Sample.objects.get(GifA=pk)
    form = SampleForm(instance=key)
    if request.method == 'POST':
        form = SampleForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/sample')
    context = {'form': form}
    return render(request, 'sample/ajout_sample.html', context)


def supprimer_sample(request, pk):
    context = {}
    obj = Sample.objects.get(GifA=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/sample')
    return render(request, 'sample/ajout_sample.html', context)


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadsample(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            from .models import Sample
            excel_file = request.FILES['file']
            fd, path = tempfile.mkstemp()  # mkstemp returns a tuple: an integer (index) called file descriptor used by OS to refer to a file and its path
            try:
                with os.fdopen(fd, 'wb') as tmp:
                    tmp.write(excel_file.read())
                book = xlrd.open_workbook(path)
                sheet = book.sheet_by_index(0)
                j = 0
                for i in range(1, sheet.nrows):
                    if Sample.objects.filter(GifA=int(sheet.cell_value(rowx=i, colx=0))).exists():
                        messages.error(request, "GifA line " + str(i + 1) + " already exists")
                        break
                    else:
                        obj = Sample(
                            GifA=int(sheet.cell_value(rowx=i, colx=0)),
                            sample_reference_blank=sheet.cell_value(rowx=i, colx=1),
                            user_sample_description=sheet.cell_value(rowx=i, colx=2),
                            submitter_1_id=People.objects.get(id=int(sheet.cell_value(rowx=i, colx=3))) if (
                                        sheet.cell_value(rowx=i, colx=3) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=3), float) and People.objects.filter(
                                    id=int(sheet.cell_value(rowx=i, colx=3))).exists()) else None,
                            submitter_2_id=People.objects.get(id=int(sheet.cell_value(rowx=i, colx=4))) if (
                                        sheet.cell_value(rowx=i, colx=4) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=4), float) and People.objects.filter(
                                    id=int(sheet.cell_value(rowx=i, colx=4))).exists()) else None,
                            project_id=Research.objects.get(id=int(sheet.cell_value(rowx=i, colx=5))) if (
                                        sheet.cell_value(rowx=i, colx=5) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=5), float) and Research.objects.filter(
                                    id=int(sheet.cell_value(rowx=i, colx=5))).exists()) else None,
                            contact_lsce_id=People.objects.get(id=int(sheet.cell_value(rowx=i, colx=6))) if (
                                        sheet.cell_value(rowx=i, colx=6) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=6), float) and People.objects.filter(
                                    id=int(sheet.cell_value(rowx=i, colx=6))).exists()) else None,
                            receipt_date=sheet.cell_value(rowx=i, colx=7) if (
                                        sheet.cell_value(rowx=i, colx=7) != "") else None,
                            expected_age=sheet.cell_value(rowx=i, colx=8),
                            expected_F14C=sheet.cell_value(rowx=i, colx=9),
                            further_information_concerning_sample=sheet.cell_value(rowx=i, colx=10),
                            research_thematic=sheet.cell_value(rowx=i, colx=11),
                            link_between_GifAs=sheet.cell_value(rowx=i, colx=12) if (
                                        sheet.cell_value(rowx=i, colx=12) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=12), float)) else None,
                            link_comment=sheet.cell_value(rowx=i, colx=13),
                            collec_science=sheet.cell_value(rowx=i, colx=14),
                            paper=Paper.objects.get(DOI=sheet.cell_value(rowx=i, colx=15)) if (
                                        sheet.cell_value(rowx=i, colx=15) != "" and Paper.objects.filter(
                                    id=sheet.cell_value(rowx=i, colx=15)).exists()) else None,
                            ocean_sea=sheet.cell_value(rowx=i, colx=16),
                            profile_core_name=sheet.cell_value(rowx=i, colx=17),
                            sampling_core_depth_cm=sheet.cell_value(rowx=i, colx=18) if (
                                        sheet.cell_value(rowx=i, colx=18) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=18), float)) else None,
                            cruise_name=sheet.cell_value(rowx=i, colx=19),
                            vessel=sheet.cell_value(rowx=i, colx=20),
                            country=sheet.cell_value(rowx=i, colx=21),
                            state_province_departement=sheet.cell_value(rowx=i, colx=22),
                            city=sheet.cell_value(rowx=i, colx=23),
                            site_name=sheet.cell_value(rowx=i, colx=24),
                            longitude=sheet.cell_value(rowx=i, colx=25) if (
                                        sheet.cell_value(rowx=i, colx=25) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=25), float)) else None,
                            latitude=sheet.cell_value(rowx=i, colx=26) if (
                                        sheet.cell_value(rowx=i, colx=26) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=26), float)) else None,
                            altitude=sheet.cell_value(rowx=i, colx=27) if (
                                        sheet.cell_value(rowx=i, colx=27) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=27), float)) else None,
                            depth=sheet.cell_value(rowx=i, colx=28) if (
                                        sheet.cell_value(rowx=i, colx=28) != "" and isinstance(
                                    sheet.cell_value(rowx=i, colx=28), float)) else None,
                            short_geographical_description=sheet.cell_value(rowx=i, colx=29),
                            associated_documents=sheet.cell_value(rowx=i, colx=30),
                            further_information=sheet.cell_value(rowx=i, colx=31),
                            fieldwork_cruise_date=sheet.cell_value(rowx=i, colx=32) if (
                                        sheet.cell_value(rowx=i, colx=32) != "") else None,
                            collected_field_by=sheet.cell_value(rowx=i, colx=33),
                            experiment_type=sheet.cell_value(rowx=i, colx=34),
                            experiment_leader=sheet.cell_value(rowx=i, colx=35),
                            short_experiment_description=sheet.cell_value(rowx=i, colx=36),
                            managing_organization=sheet.cell_value(rowx=i, colx=37),
                            institution_name=sheet.cell_value(rowx=i, colx=38),
                            further_information_2=sheet.cell_value(rowx=i, colx=39),
                            sampling_depth=sheet.cell_value(rowx=i, colx=40),
                            object_ID=sheet.cell_value(rowx=i, colx=41),
                            description=sheet.cell_value(rowx=i, colx=42),
                            sample_type=sheet.cell_value(rowx=i, colx=43),
                            sample_fraction_analysed=sheet.cell_value(rowx=i, colx=44),
                            additional_information_material=sheet.cell_value(rowx=i, colx=45),
                            raw_sample_weight=sheet.cell_value(rowx=i, colx=46) if (
                                        sheet.cell_value(rowx=i, colx=46) != "") else None,
                            potential_contamination=sheet.cell_value(rowx=i, colx=47),
                            collection_protocol=sheet.cell_value(rowx=i, colx=48),
                            further_information_3=sheet.cell_value(rowx=i, colx=49),
                            sub_sampling_date=sheet.cell_value(rowx=i, colx=50) if (
                                        sheet.cell_value(rowx=i, colx=50) != "") else None,
                            sub_sample_collected_by=sheet.cell_value(rowx=i, colx=51),
                            sub_sample_identified_by=sheet.cell_value(rowx=i, colx=52),
                            nature_fraction_be_analyse=sheet.cell_value(rowx=i, colx=53),
                            date_sub_sampling=sheet.cell_value(rowx=i, colx=54) if (
                                        sheet.cell_value(rowx=i, colx=54) != "") else None,
                            sub_sample_collection_protocol=sheet.cell_value(rowx=i, colx=55),
                            subsample_weight_mg=sheet.cell_value(rowx=i, colx=56),
                        )
                        obj.save()
                        j += 1
                messages.success(request, str(j) + " lines have been downloaded")
            finally:
                os.remove(path)

        else:
            return redirect('/sample/')
    else:
        form = UploadFileForm()
    return render(request, 'sample/upload_sample.html', {'form': form})
