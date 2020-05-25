from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import (DepartmentModel,
                     ModuleModel,
                     TargetModel,
                     ModuleTargetModel,
                     DepartmentModuleModel,
                     DepartmentGroupModel
                     )
from django import forms


class DepartmentNewForm(ModelForm):
    class Meta:
        model = DepartmentModel
        fields = ['department']

    def clean_department(self):
        department = self.cleaned_data.get('department').lower()
        if department:
            if DepartmentModel.objects.filter(department=department).exists():
                raise ValidationError("The Department Name Already exist")
            else:
                if DepartmentModel.objects.filter(slug=slugify(department)).exists():
                    raise ValidationError("The Department already exist.")
        else:
            raise ValidationError("Department cannot be empty")
        return department


class DepartmentUpdateForm(ModelForm):
    class Meta:
        model = DepartmentModel
        fields = ['department', 'status']

    def clean(self):
        department = self.cleaned_data.get('department').lower()
        status = self.cleaned_data.get('status')

        if department:
            if DepartmentModel.objects.filter(department=department, status=status).exists():
                raise ValidationError("You need to make some change in order to update the department details.")
        else:
            raise ValidationError("Department cannot be empty")
        return self.cleaned_data


class ModuleNewForm(ModelForm):
    class Meta:
        model = ModuleModel
        fields = ['module']

    def clean_module(self):
        module = self.cleaned_data.get('module').lower()
        if module:
            if ModuleModel.objects.filter(module=module).exists():
                raise ValidationError("The Module Name Already exist")
            else:
                if ModuleModel.objects.filter(slug=slugify(module)).exists():
                    raise ValidationError("The Module already exist.")
        else:
            raise ValidationError("Module cannot be empty")
        return module


class ModuleUpdateForm(ModelForm):
    class Meta:
        model = ModuleModel
        fields = ['module', 'status']

    def clean(self):
        module = self.cleaned_data.get('module').lower()
        status = self.cleaned_data.get('status')

        if not module:
            raise ValidationError("Module cannot be empty")
        #     if ModuleModel.objects.filter(module=module, status=status).exists():
        #         raise ValidationError("You need to make some change in order to update the module details.")
        # else:

        return self.cleaned_data


class TargetNewForm(ModelForm):
    class Meta:
        model = TargetModel
        fields = ['target']

    def clean_module(self):
        target = self.cleaned_data.get('target').lower()
        if target:
            if TargetModel.objects.filter(target=target).exists():
                raise ValidationError("The Target Name Already exist")
            else:
                if TargetModel.objects.filter(slug=slugify(target)).exists():
                    raise ValidationError("The Target already exist.")
        else:
            raise ValidationError("Target cannot be empty")
        return target


class TargetUpdateForm(ModelForm):
    class Meta:
        model = TargetModel
        fields = ['target', 'status']

    def clean(self):
        target = self.cleaned_data.get('target').lower()
        status = self.cleaned_data.get('status')

        if target:
            if TargetModel.objects.filter(target=target, status=status).exists():
                raise ValidationError("You need to make some change in order to update the module details.")
        else:
            raise ValidationError("Target cannot be empty")
        return self.cleaned_data


class ModuleTargetMapNewForm(ModelForm):
    class Meta:
        model = ModuleTargetModel
        fields = ['module', 'target']

    def clean(self):
        module = self.cleaned_data.get('module')
        target = self.cleaned_data.get('target')
        if target and module:
            module = ModuleModel.objects.filter(slug=module).first()
            if module:
                target = TargetModel.objects.filter(slug=target).first()
                if target:
                    if ModuleTargetModel.objects.filter(target=target, module=module).exists():
                        raise ValidationError("Mapping between the Module and Target Already exist. "
                                              "Please check and try again")
                else:
                    raise ValidationError("Target doesnot exist. Please check again.")
            else:
                raise ValidationError("Module does not exist. please check again")
        else:
            raise ValidationError("You need to provide both Module and Target")
        return self.cleaned_data


class ModuleTargetUpdateForm(ModelForm):
    class Meta:
        model = ModuleTargetModel
        fields = ['module', 'target', 'status']

    def clean(self):
        module = self.cleaned_data.get('module')
        target = self.cleaned_data.get('target')
        status = self.cleaned_data.get('status')

        if target and module:
            module = ModuleModel.objects.filter(slug=module).first()
            if module:
                target = TargetModel.objects.filter(slug=target).first()
                if target:
                    if ModuleTargetModel.objects.filter(target=target, module=module, status=status).exists():
                        raise ValidationError("Mapping between the Module and Target Already exist. "
                                              "Please check and try again")
                else:
                    raise ValidationError("Target doesnot exist. Please check again.")
            else:
                raise ValidationError("Module does not exist. please check again")
        else:
            raise ValidationError("You need to provide both Module and Target")
        return self.cleaned_data


class DepartmentModuleMapNewForm(ModelForm):
    class Meta:
        model = DepartmentModuleModel
        fields = ['department', 'module']

    def clean(self):
        department = self.cleaned_data.get('department')
        module = self.cleaned_data.get('module')
        if department and module:
            department = DepartmentModel.objects.filter(slug=department).first()
            if department:
                module = ModuleModel.objects.filter(slug=module).first()
                if module:
                    if DepartmentModuleModel.objects.filter(department=department, module=module).exists():
                        raise ValidationError("Mapping between the department and module Already exist. "
                                              "Please check and try again")
                else:
                    raise ValidationError("Module does exist. Please check again.")
            else:
                raise ValidationError("Department does not exist. please check again")
        else:
            raise ValidationError("You need to provide both Department and Module")
        return self.cleaned_data


class DepartmentModuleUpdateForm(ModelForm):
    class Meta:
        model = DepartmentModuleModel
        fields = ['department', 'module', 'status']

    def clean(self):
        department = self.cleaned_data.get('department')
        module = self.cleaned_data.get('module')
        status = self.cleaned_data.get('status')

        if department and module:
            department = DepartmentModel.objects.filter(slug=department).first()
            if department:
                module = ModuleModel.objects.filter(slug=module).first()
                if module:
                    if DepartmentModuleModel.objects.filter(department=department, module=module, status=status).exists():
                        raise ValidationError("Mapping between the department and module Already exist. "
                                              "Please check and try again")
                else:
                    raise ValidationError("Module doesnot exist. Please check again.")
            else:
                raise ValidationError("Department does not exist. please check again")
        else:
            raise ValidationError("You need to provide both Department and Module")
        return self.cleaned_data


class DepartmentGroupNewForm(ModelForm):
    class Meta:
        model = DepartmentGroupModel
        fields = ['department', 'group']

    def clean(self):
        department = self.cleaned_data.get('department')
        group = self.cleaned_data.get('group')

        if department:
            department = DepartmentModel.objects.filter(slug=department).first()
            if department:
                if group:
                    if DepartmentGroupModel.objects.filter(department=department, group=group).exists():
                        raise ValidationError("The department and department_group name already exist. please check and try again")
                else:
                    raise ValidationError("Group name is mandatory and cannot be left blank. please enter the value.")
            else:
                raise ValidationError("Selected Department doesnot exist. please check and try again")
        else:
            raise ValidationError("You need to select one Department")
        return self.cleaned_data


class DepartmentGroupUpdateForm(ModelForm):
    class Meta:
        model = DepartmentGroupModel
        fields = ['department', 'group', 'status']

    def clean(self):
        department = self.cleaned_data.get('department')
        group = self.cleaned_data.get('group')
        status = self.cleaned_data.get('status')

        if department and group:
            department = DepartmentModel.objects.filter(slug=department).first()
            if department:
                if group:
                    if DepartmentGroupModel.objects.filter(department=department, group=group, status=status).exists():
                        raise ValidationError("Mapping between the department and group Already exist. "
                                              "Please check and try again")
                else:
                    raise ValidationError("Group doesnot exist. Please check again.")
            else:
                raise ValidationError("Department does not exist. please check again")
        else:
            raise ValidationError("You need to provide both Department and Group")
        return self.cleaned_data


class ModuleMapWithTargetForm(forms.Form):
    target = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def clean(self):
        targets = self.cleaned_data.get("target", False)
        if not targets:
            raise ValidationError("While submitting you need to select at least one target for mapping.")
        return self.cleaned_data