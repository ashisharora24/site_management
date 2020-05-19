from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import DepartmentNewForm, DepartmentUpdateForm
from .models import DepartmentModel


# Create your views here.
def home(request):
    template_name = 'site_management/home.html'
    context = {}
    return render(request, template_name, context)

# ----------------------------------------------------------------------------


def department_new(request):
    template_name = 'site_management/department/new.html'
    context = {}
    form = DepartmentNewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'New Department added.')
            form = DepartmentNewForm()
    context['form'] = form
    department_obj = DepartmentModel.objects.all()
    context['department_obj'] = department_obj

    return render(request, template_name, context)


def department_list(request):
    template_name = 'site_management/department/list.html'
    context = {}
    department_obj = DepartmentModel.objects.all()
    context['department_obj'] = department_obj

    return render(request, template_name, context)


def department_specific(request, slug):
    template_name = 'site_management/department/specific.html'
    context = {}
    department_obj = DepartmentModel.objects.filter(slug=slug).first()
    context['department_obj'] = department_obj
    return render(request, template_name, context)


def department_update(request, slug):
    template_name = 'site_management/department/update.html'
    context = {}
    department_obj = DepartmentModel.objects.get(slug=slug)
    form = DepartmentUpdateForm(request.POST or None, instance=department_obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Department details updated successfully.')
            return redirect('/site_management/department/list/')
    context['form'] = form
    return render(request, template_name, context)


def department_delete(request, slug):
    template_name = 'site_management/department/delete.html'
    context = {}
    department_obj = DepartmentModel.objects.filter(slug=slug).first()
    context['department_obj'] = department_obj
    if request.method == 'POST':
        if request.POST['agree']:
            DepartmentModel.objects.filter(slug=slug).first().delete()
            messages.success(request, 'Department deleted successfully.')
            return redirect('/site_management/department/list/')
    return render(request, template_name, context)
# ----------------------------------------------------------------------------