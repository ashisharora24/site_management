from django.contrib import admin

from .models import (   ModuleModel,
                        TargetModel,
                        ModuleTargetModel,
                        DepartmentModel,
                        DepartmentModuleModel,
                        DepartmentGroupModel,
                        DepartmentGroupModuleTargetModel,
                        UserDepartmentModel,
                        UserDepartmentGroupModel,
                        UserDepartmentModuleTargetModel
                    )

# Register your models here.
admin.site.register(ModuleModel)
admin.site.register(TargetModel)
admin.site.register(ModuleTargetModel)
admin.site.register(DepartmentModel)
admin.site.register(DepartmentModuleModel)
admin.site.register(DepartmentGroupModel)
admin.site.register(DepartmentGroupModuleTargetModel)
admin.site.register(UserDepartmentModel)
admin.site.register(UserDepartmentGroupModel)
admin.site.register(UserDepartmentModuleTargetModel)