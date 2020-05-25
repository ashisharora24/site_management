from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from .forms import DepartmentNewForm, DepartmentUpdateForm, ModuleMapWithTargetForm
from .forms import (ModuleNewForm, ModuleUpdateForm,
                    TargetNewForm, TargetUpdateForm,
                    ModuleTargetMapNewForm, ModuleTargetUpdateForm,
                    DepartmentModuleMapNewForm, DepartmentModuleUpdateForm,
                    DepartmentGroupNewForm, DepartmentGroupUpdateForm
                    )
from .models import (DepartmentModel,
                     ModuleModel,
                     TargetModel,
                     ModuleTargetModel,
                     DepartmentModuleModel,
                     DepartmentGroupModel
                     )


from .querys import *
from django import forms

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
            obj = form.save()
            messages.success(request, 'New Department added.')
            return HttpResponseRedirect(reverse('site_management__department__map', args=(obj.slug,)))
            # form = DepartmentNewForm()
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


def department_module_target_saving(department_slug: str = None, update_module_target_slug_list: list = []):
    department_obj = DepartmentModel.objects.filter(slug=department_slug).first()
    current_dep_mod_tar_obj = DepartmentModuleTargetModel.objects.filter(department=department_obj)
    cu_de_mod_tar_list = [i.slug for i in current_dep_mod_tar_obj]
    up_de_mod_tar_list = ["{dep_slug}_{i}".format(dep_slug=department_slug, i=i) for i in update_module_target_slug_list]
    add_list = set(up_de_mod_tar_list)-set(cu_de_mod_tar_list)
    delete_list = set(cu_de_mod_tar_list)-set(up_de_mod_tar_list)
    for i in delete_list:
        DepartmentModuleTargetModel.objects.filter(slug=i).delete()
    for dmts in add_list:
        ds,ms,ts = dmts.split("_")
        module_target_obj = ModuleTargetModel.objects.filter(slug="{ms}_{ts}".format(ms=ms, ts=ts)).first()
        DepartmentModuleTargetModel(department=department_obj,
                                    module_target=module_target_obj,
                                    slug=dmts
                                    ).save()


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
    context['department'] = DepartmentModel.objects.filter(slug=slug).first()
    context['module_target_with_department_status'] = department_module_target_mapping_query(slug)
    return render(request, template_name, context)


def department_mapping_with_module_target(request, slug):
    template_name = 'site_management/department/department_module_target_mapping.html'
    context = {}
    if request.method == 'POST':
        module_target_list = request.POST.getlist("department_module_target")
        department_module_target_saving(department_slug=slug,
                                        update_module_target_slug_list=module_target_list)
    context['department'] = DepartmentModel.objects.filter(slug=slug).first()
    context['module_target_with_department_status'] = department_module_target_mapping_query(slug)
    return render(request, template_name, context)
# ----------------------------------------------------------------------------


def module_new(request):
    template_name = 'site_management/module/new.html'
    context = {}
    form = ModuleNewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'New Module added.')
            print(obj.slug)
            return HttpResponseRedirect(reverse('site_management__module__target_mapping', args=(obj.slug,)))
    context['form'] = form
    module_obj = ModuleModel.objects.all()
    context['module_obj'] = module_obj

    return render(request, template_name, context)

def module_target_mapping_update(slug, target_slug_list):
    module_obj = ModuleModel.objects.filter(slug=slug).first()
    ModuleTargetModel.objects.filter(module=module_obj).delete()
    for target_slug in target_slug_list:
        target_obj = TargetModel.objects.filter(slug=target_slug).first()
        ModuleTargetModel(target=target_obj, module=module_obj).save()

def module_target_mapping(request, slug):

    template_name = 'site_management/module/module_target_mapping.html'
    context = {}

    target_objects, module_target_object = module_target_mapping_query(slug)
    # the
    form = ModuleMapWithTargetForm(request.POST or None)
    form.fields['target'].choices = [(target.slug, target.target) for target in target_objects]
    form.fields['target'].initial = [module_target.target.slug for module_target in module_target_object]
    if form.is_valid():
        target_slug_list = request.POST.getlist('target')
        module_obj = ModuleModel.objects.filter(slug=slug).first()
        ModuleTargetModel.objects.filter(module=module_obj).delete()
        for target_slug in target_slug_list:
            target_obj = TargetModel.objects.filter(slug=target_slug).first()
            ModuleTargetModel(target=target_obj, module=module_obj).save()
        return HttpResponseRedirect(reverse('site_management__module__specific', args=(slug,)))
    context['form'] = form
    context['module'] = ModuleModel.objects.filter(slug=slug).first()
    return render(request, template_name, context)


def module_list(request):
    template_name = 'site_management/module/list.html'
    context = {}
    module_obj = ModuleModel.objects.all()
    context['module_obj'] = module_obj
    return render(request, template_name, context)


def module_specific(request, slug):
    template_name = 'site_management/module/specific.html'
    context = {}
    module_obj = ModuleModel.objects.filter(slug=slug).first()
    context['module_obj'] = module_obj

    target_objects, module_target_object = module_target_mapping_query(slug)
    context['module_target_object'] = module_target_object

    return render(request, template_name, context)

def module_update(request, slug):
    template_name = 'site_management/module/update.html'
    context = {}
    module_obj = ModuleModel.objects.get(slug=slug)
    form = ModuleUpdateForm(request.POST or None, instance=module_obj)

    target_objects, module_target_object = module_target_mapping_query(slug)
    # the
    form1 = ModuleMapWithTargetForm(request.POST or None)
    form1.fields['target'].choices = [(target.slug, target.target) for target in target_objects]
    form1.fields['target'].initial = [module_target.target.slug for module_target in module_target_object]

    if request.method == "POST":
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Module details updated successfully.')
            target_slug_list = request.POST.getlist('target')
            module_target_mapping_update(str(obj), target_slug_list)
            return redirect('/site_management/module/list/')
    context['form'] = form
    context['form1'] = form1
    return render(request, template_name, context)


def module_delete(request, slug):
    template_name = 'site_management/module/delete.html'
    context = {}
    module_obj = ModuleModel.objects.filter(slug=slug).first()
    context['module_obj'] = module_obj
    if request.method == 'POST':
        if request.POST['agree']:
            ModuleModel.objects.filter(slug=slug).first().delete()
            messages.success(request, 'Module deleted successfully.')
            return redirect('/site_management/module/list/')
    return render(request, template_name, context)
# ----------------------------------------------------------------------------


def target_new(request):
    template_name = 'site_management/target/new.html'
    context = {}
    form = TargetNewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'New Target added.')
            form = TargetNewForm()
    context['form'] = form
    target_obj = TargetModel.objects.all()
    context['target_obj'] = target_obj

    return render(request, template_name, context)


def target_list(request):
    template_name = 'site_management/target/list.html'
    context = {}
    target_obj = TargetModel.objects.all()
    context['target_obj'] = target_obj

    return render(request, template_name, context)


def target_specific(request, slug):
    template_name = 'site_management/target/specific.html'
    context = {}
    target_obj = TargetModel.objects.filter(slug=slug).first()
    context['target_obj'] = target_obj
    return render(request, template_name, context)


def target_update(request, slug):
    template_name = 'site_management/target/update.html'
    context = {}
    target_obj = TargetModel.objects.get(slug=slug)
    form = TargetUpdateForm(request.POST or None, instance=target_obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Target details updated successfully.')
            return redirect('/site_management/target/list/')
    context['form'] = form
    return render(request, template_name, context)


def target_delete(request, slug):
    template_name = 'site_management/target/delete.html'
    context = {}
    target_obj = TargetModel.objects.filter(slug=slug).first()
    context['target_obj'] = target_obj
    if request.method == 'POST':
        if request.POST['agree']:
            TargetModel.objects.filter(slug=slug).first().delete()
            messages.success(request, 'Target deleted successfully.')
            return redirect('/site_management/target/list/')
    return render(request, template_name, context)
# ----------------------------------------------------------------------------


def module_target_map_new(request):
    template_name = 'site_management/module_target_map/new.html'
    context = {}
    form = ModuleTargetMapNewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'New Target added.')
            form = ModuleTargetMapNewForm()
    context['form'] = form
    context['module_target_object'] = module_target_query()
    return render(request, template_name, context)


def module_target_map_list(request):
    template_name = 'site_management/module_target_map/list.html'
    context = {'module_target_object': module_target_query()}
    return render(request, template_name, context)


def module_target_specific(request, slug):
    template_name = 'site_management/module_target_map/specific.html'
    context = {}
    module_target_obj = ModuleTargetModel.objects.filter(slug=slug).first()
    context['module_target_obj'] = module_target_obj
    return render(request, template_name, context)


def module_target_update(request, slug):
    template_name = 'site_management/module_target_map/update.html'
    context = {}
    module_target_obj = ModuleTargetModel.objects.get(slug=slug)
    print(module_target_obj)
    form = ModuleTargetUpdateForm(request.POST or None, instance=module_target_obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Module Target Mapping details updated successfully.')
            return redirect('/site_management/module_target_map/list/')
    context['form'] = form
    return render(request, template_name, context)


def module_target_delete(request, slug):
    template_name = 'site_management/target/delete.html'
    context = {}
    module_target_obj = ModuleTargetModel.objects.filter(slug=slug).first()
    context['module_target_obj'] = module_target_obj
    if request.method == 'POST':
        if request.POST['agree']:
            ModuleTargetModel.objects.filter(slug=slug).first().delete()
            messages.success(request, 'Module Target mapping deleted successfully.')
            return redirect('/site_management/module_target_map/list/')
    return render(request, template_name, context)
# ----------------------------------------------------------------------------


def department_module_map_new(request):
    template_name = 'site_management/department_module_map/new.html'
    context = {}
    form = DepartmentModuleMapNewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'New document module mapping added.')
            form = DepartmentModuleMapNewForm()
    context['form'] = form
    department_module_obj = DepartmentModuleModel.objects.all()
    context['department_module_obj'] = department_module_obj
    return render(request, template_name, context)


def department_module_map_list(request):
    template_name = 'site_management/department_module_map/list.html'
    context = {}
    department_module_obj = DepartmentModuleModel.objects.all()
    context['department_module_obj'] = department_module_obj
    return render(request, template_name, context)


def department_module_specific(request, slug):
    template_name = 'site_management/department_module_map/specific.html'
    context = {}
    department_module_obj = DepartmentModuleModel.objects.filter(slug=slug).first()
    context['department_module_obj'] = department_module_obj
    return render(request, template_name, context)


def department_module_update(request, slug):
    template_name = 'site_management/department_module_map/update.html'
    context = {}
    department_module_obj = DepartmentModuleModel.objects.get(slug=slug)
    print(department_module_obj)
    form = DepartmentModuleUpdateForm(request.POST or None, instance=department_module_obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Department ModuleMapping details updated successfully.')
            return redirect('/site_management/department_module_map/list/')
    context['form'] = form
    return render(request, template_name, context)


def department_module_delete(request, slug):
    template_name = 'site_management/department_module_map/delete.html'
    context = {}
    department_module_obj = DepartmentModuleModel.objects.filter(slug=slug).first()
    context['department_module_obj'] = department_module_obj
    if request.method == 'POST':
        if request.POST['agree']:
            DepartmentModuleModel.objects.filter(slug=slug).first().delete()
            messages.success(request, 'Department Module mapping deleted successfully.')
            return redirect('/site_management/department_module_map/list/')
    return render(request, template_name, context)
# ----------------------------------------------------------------------------


def department_group_new(request):
    template_name = "site_management/department_group/new.html"
    context = {}
    form = DepartmentGroupNewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Group added for the specified Department')
            form = DepartmentGroupNewForm()
    context['form'] = form
    department_group_obj = DepartmentGroupModel.objects.all()
    context['department_group_obj'] = department_group_obj
    return render(request, template_name, context)


def department_group_list(request):
    template_name = 'site_management/department_group/list.html'
    context = {}
    department_group_obj = DepartmentGroupModel.objects.all()
    context['department_group_obj'] = department_group_obj
    return render(request, template_name, context)


def department_group_specific(request, slug):
    template_name = 'site_management/department_group/specific.html'
    context = {}
    department_group_obj = DepartmentGroupModel.objects.filter(slug=slug).first()
    context['department_group_obj'] = department_group_obj
    return render(request, template_name, context)


def department_group_update(request, slug):
    template_name = 'site_management/department_group/update.html'
    context = {}
    department_group_obj = DepartmentGroupModel.objects.get(slug=slug)
    form = DepartmentGroupUpdateForm(request.POST or None, instance=department_group_obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Department ModuleMapping details updated successfully.')
            return redirect('/site_management/department_group/list/')
    context['form'] = form
    return render(request, template_name, context)


def department_group_delete(request, slug):
    template_name = 'site_management/department_group/delete.html'
    context = {}
    department_group_obj = DepartmentGroupModel.objects.filter(slug=slug).first()
    context['department_group_obj'] = department_group_obj
    if request.method == 'POST':
        if request.POST['agree']:
            DepartmentGroupModel.objects.filter(slug=slug).first().delete()
            messages.success(request, 'Department Module mapping deleted successfully.')
            return redirect('/site_management/department_group/list/')
    return render(request, template_name, context)