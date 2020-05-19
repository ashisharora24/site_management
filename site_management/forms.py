from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import DepartmentModel


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
