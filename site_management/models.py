from django.db import models
from django.conf import settings
from django.utils.text import slugify
User = settings.AUTH_USER_MODEL


# Create your models here.
class ModuleModel(models.Model):
    module = models.CharField(max_length=120)
    slug = models.SlugField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug


class TargetModel(models.Model):
    target = models.CharField(max_length=120)
    slug = models.SlugField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug


class ModuleTargetModel(models.Model):
    module = models.ForeignKey(ModuleModel, on_delete=models.CASCADE)
    target = models.ForeignKey(TargetModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{module}-{target}".format(self.module, self.target)


class DepartmentModel(models.Model):
    department = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if self.department:
            self.department = self.department.lower()
            self.slug = slugify(self.department)
        super(DepartmentModel, self).save(*args, **kwargs)


class DepartmentModuleModel(models.Model):
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{department}-{module}".format(self.department, self.module)


class DepartmentGroupModel(models.Model):
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    group = models.CharField(max_length=120)
    slug = models.SlugField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{department}-{group}".format(self.department, self.group)


class DepartmentGroupModuleModel(models.Model):
    department_group = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{department_group}-{module}".format(department_group=self.department_group, module=self.module)


class UserDepartmentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{user}-{department}".format(user=self.user, department=self.department)


class UserDepartmentGroupModel(models.Model):
    user_department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE)
    department_group = models.ForeignKey(DepartmentGroupModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{user_department}-{department_group}".format(user_deparmtent=self.user_department,
                                                             department_group=self.department_group)

class UserDepartmentModuleTargetModel(models.Model):
    user_department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE)
    module_target = models.ForeignKey(ModuleTargetModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{user_department}-{module_target}".format(user_deparmtent=self.user_department,
                                                             module_target=self.module_target)