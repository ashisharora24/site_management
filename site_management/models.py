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

    def save(self, *args, **kwargs):
        if self.module:
            self.module = self.module.lower()
            self.slug = slugify(self.module)
        super(ModuleModel, self).save(*args, **kwargs)


class TargetModel(models.Model):
    target = models.CharField(max_length=120)
    slug = models.SlugField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if self.target:
            self.target = self.target.lower()
            self.slug = slugify(self.target)
        super(TargetModel, self).save(*args, **kwargs)


class ModuleTargetModel(models.Model):
    module = models.ForeignKey(ModuleModel, on_delete=models.CASCADE)
    target = models.ForeignKey(TargetModel, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if self.target and self.module:
            self.slug = slugify(str(self.module)+"_"+str(self.target))
            self.target = TargetModel.objects.filter(slug=self.target).first()
            self.module = ModuleModel.objects.filter(slug=self.module).first()
        super(ModuleTargetModel, self).save(*args, **kwargs)


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
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if self.department and self.module:
            self.slug = slugify(str(self.department)+"_"+str(self.module))
            self.department = DepartmentModel.objects.filter(slug=self.department).first()
            self.module = ModuleModel.objects.filter(slug=self.module).first()
        super(DepartmentModuleModel, self).save(*args, **kwargs)


class DepartmentGroupModel(models.Model):
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    group = models.CharField(max_length=120, unique=True)
    slug = models.SlugField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if self.group:
            self.group = self.group.lower()
            self.slug = slugify(str(self.department)+"_"+str(self.group))
        super(DepartmentGroupModel, self).save(*args, **kwargs)


class DepartmentGroupModuleTargetModel(models.Model):
    department_group = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    module_target = models.ForeignKey(ModuleTargetModel, on_delete=models.CASCADE)
    slug = models.SlugField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slug


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