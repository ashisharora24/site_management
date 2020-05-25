from .models import *


def module_target_query():
    # module_target = [{module:[{targets:module_target},]}]
    module_target = []
    module_obj = ModuleModel.objects.all()
    for module in module_obj:
        target_list = ModuleTargetModel.objects.filter(module=module)
        module_target.append({module: {len(target_list): target_list}})
    return module_target


def module_target_mapping_query(module_slug: str = None):
    """
    :parameter: module
    :type: str
    :returns:
    1.  object : Target Module
        all the targets which are right now with status= True
    2.  object : ModuleTargetModel
        all the target(status=True) slug which are mapped with Module and has a mapping status as true
    """
    # first we will get the list of all the target object
    target_objects = TargetModel.objects.filter(status=True)
    # now we need to get the list of all the objects of targets which are already mapped with the module
    # for this first we will get the module object
    module_object = ModuleModel.objects.filter(slug=module_slug).first()
    # once we got the module object, we will now get all the module_target objects which have a true status
    module_target_object = ModuleTargetModel.objects.filter(module=module_object).filter(
        target__in=target_objects).filter(status=True)

    return target_objects, module_target_object


def department_module_target_mapping_query(department_slug: str = None):
    module_target_with_department_status = []
    department_obj = DepartmentModel.objects.filter(slug=department_slug).first()
    module_object = ModuleModel.objects.filter(status=True)
    target_object = TargetModel.objects.filter(status=True)

    for module in module_object:
        module_target_object = ModuleTargetModel.objects.filter(module=module).filter(target__in=target_object).filter(
            status=True)
        list = []
        for module_target in module_target_object:
            if DepartmentModuleTargetModel.objects.filter(department=department_obj).filter(
                    module_target__slug=module_target.slug).exists():
                list.append([module_target, True])
                continue
            list.append([module_target, False])
        module_target_with_department_status.append([module,len(module_target_object), list])
    return module_target_with_department_status
