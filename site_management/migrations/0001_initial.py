# Generated by Django 3.0.6 on 2020-05-17 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_group', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleTargetModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.ModuleModel')),
            ],
        ),
        migrations.CreateModel(
            name='TargetModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartmentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.DepartmentModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartmentModuleTargetModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('module_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.ModuleTargetModel')),
                ('user_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.UserDepartmentModel')),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartmentGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('department_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.DepartmentGroupModel')),
                ('user_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.UserDepartmentModel')),
            ],
        ),
        migrations.AddField(
            model_name='moduletargetmodel',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.TargetModel'),
        ),
        migrations.CreateModel(
            name='DepartmentModuleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.DepartmentModel')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.ModuleModel')),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentGroupModuleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('department_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.DepartmentModel')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.ModuleModel')),
            ],
        ),
        migrations.AddField(
            model_name='departmentgroupmodel',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_management.DepartmentModel'),
        ),
    ]
