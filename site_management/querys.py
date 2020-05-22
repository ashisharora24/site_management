from .models import ModuleModel, TargetModel, ModuleTargetModel


# def module_target_query():
#     # module_target = [{module:[{targets:module_target},]}]
#     module_target = []
#     module_obj = ModuleModel.objects.all()
#     for module in module_obj:
#         target_list = ModuleTargetModel.objects.filter(module=module)
#
#         module_target.append({module: target_list})
#     return module_target

def module_target_query():
    # module_target = [{module:[{targets:module_target},]}]
    module_target = []
    module_obj = ModuleModel.objects.all()
    for module in module_obj:
        target_list = ModuleTargetModel.objects.filter(module=module)
        module_target.append({module: {len(target_list): target_list}})
    return module_target
