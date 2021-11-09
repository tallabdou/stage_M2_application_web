from django.shortcuts import render, redirect
from .forms import StandardsForm
from .models import Standards
from .filters import StandardsFiltre
from django.http import HttpResponse
import xlwt
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def list_standards(request):
    standardss = Standards.objects.all()
    myFilter = StandardsFiltre(request.GET, queryset=standardss)
    standardss = myFilter.qs
    if request.GET.get('Export') == 'Export':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="standards.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('standards')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [f.name for f in Standards._meta.concrete_fields]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = standardss.values_list()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response
    context = {'standardss': standardss, 'myFilter': myFilter}
    return render(request, 'standards/standards.html', context)


@login_required(login_url='login')
def ajouter_standards(request):
    form = StandardsForm()
    if request.method == 'POST':
        form = StandardsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/standards/')
    context = {'form': form}
    return render(request, 'standards/ajout_standards.html', context)


@login_required(login_url='login')
def modifier_standards(request, pk):
    key = Standards.objects.get(std_number=pk)
    form = StandardsForm(instance=key)
    if request.method == 'POST':
        form = StandardsForm(request.POST, instance=key)
        if form.is_valid():
            form.save()
            return redirect('/standards')
    context = {'form': form}
    return render(request, 'standards/ajout_standards.html', context)


def supprimer_standards(request, pk):
    context = {}
    obj = Standards.objects.get(std_number=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('/standards')
    return render(request, 'standards/ajout_standards.html', context)
