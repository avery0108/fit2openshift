# Generated by Django 2.1.2 on 2018-11-27 03:38

import common.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdHoc',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('pattern', models.CharField(default='all', max_length=1024, verbose_name='Pattern')),
                ('module', models.CharField(default='command', max_length=128, verbose_name='Module')),
                ('args', common.models.JsonTextField(verbose_name='Args')),
                ('execute_times', models.IntegerField(default=0)),
                ('created_by', models.CharField(blank=True, default='', max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdHocExecution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('timedelta', models.FloatField(default=0.0, null=True, verbose_name='Time')),
                ('state', models.CharField(choices=[('PENDING', 'Pending'), ('STARTED', 'Started'), ('SUCCESS', 'Success'), ('FAILURE', 'Failure'), ('RETRY', 'Retry')], default='PENDING', max_length=16)),
                ('num', models.IntegerField(default=1)),
                ('result_summary', common.models.JsonDictTextField(blank=True, default='{}', null=True, verbose_name='Result summary')),
                ('result_raw', common.models.JsonDictTextField(blank=True, default='{}', null=True, verbose_name='Result raw')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('date_start', models.DateTimeField(null=True, verbose_name='Start time')),
                ('date_end', models.DateTimeField(null=True, verbose_name='End time')),
                ('adhoc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ansible_api.AdHoc')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClusterGroup',
            fields=[
                ('name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(message='Enter a valid name consisting of Unicode letters, numbers, underscores, or hyphens, or dot', regex='^[a-zA-Z0-9_\\-\\.]+$')])),
                ('vars', common.models.JsonDictTextField(default={})),
                ('meta', common.models.JsonDictTextField(default={})),
                ('comment', models.TextField(blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('children', models.ManyToManyField(blank=True, related_name='parents', to='ansible_api.ClusterGroup')),
            ],
        ),
        migrations.CreateModel(
            name='ClusterHost',
            fields=[
                ('name', models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(message='Enter a valid name consisting of Unicode letters, numbers, underscores, or hyphens, or dot', regex='^[a-zA-Z0-9_\\-\\.]+$')])),
                ('ip', models.GenericIPAddressField(null=True)),
                ('port', models.IntegerField(default=22)),
                ('username', models.CharField(default='root', max_length=1024)),
                ('password', common.models.EncryptCharField(blank=True, max_length=4096, null=True)),
                ('private_key', common.models.EncryptCharField(blank=True, max_length=8192, null=True)),
                ('vars', common.models.JsonDictTextField(default={})),
                ('meta', common.models.JsonDictTextField(default={})),
                ('comment', models.TextField(blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(message='Enter a valid name consisting of Unicode letters, numbers, underscores, or hyphens, or dot', regex='^[a-zA-Z0-9_\\-\\.]+$')])),
                ('vars', common.models.JsonDictTextField(default={})),
                ('meta', common.models.JsonDictTextField(default={})),
                ('comment', models.TextField(blank=True)),
                ('children', models.ManyToManyField(blank=True, related_name='parents', to='ansible_api.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(message='Enter a valid name consisting of Unicode letters, numbers, underscores, or hyphens, or dot', regex='^[a-zA-Z0-9_\\-\\.]+$')])),
                ('ip', models.GenericIPAddressField(null=True)),
                ('port', models.IntegerField(default=22)),
                ('username', models.CharField(default='root', max_length=1024)),
                ('password', common.models.EncryptCharField(blank=True, max_length=4096, null=True)),
                ('private_key', common.models.EncryptCharField(blank=True, max_length=8192, null=True)),
                ('vars', common.models.JsonDictTextField(default={})),
                ('meta', common.models.JsonDictTextField(default={})),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Name')),
                ('pattern', models.CharField(default='all', max_length=1024, verbose_name='Pattern')),
                ('gather_facts', models.BooleanField(default=False)),
                ('vars', common.models.JsonDictTextField(blank=True, null=True, verbose_name='Vars')),
                ('tasks', common.models.JsonListTextField(blank=True, null=True, verbose_name='Tasks')),
                ('roles', common.models.JsonListTextField(blank=True, null=True, verbose_name='Roles')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Playbook',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.SlugField(allow_unicode=True, max_length=128, verbose_name='Name')),
                ('alias', models.CharField(blank=True, default='site.yml', max_length=128)),
                ('type', models.CharField(choices=[('json', 'json'), ('text', 'text'), ('file', 'file'), ('git', 'git'), ('http', 'http')], default='json', max_length=16)),
                ('git', common.models.JsonDictCharField(default={'branch': 'master', 'repo': ''}, max_length=4096)),
                ('url', models.URLField(blank=True, verbose_name='http url')),
                ('pull_policy', models.CharField(choices=[('if_not_present', 'Always'), ('always', 'If not present'), ('never', 'Never')], default='if_not_present', max_length=16)),
                ('is_periodic', models.BooleanField(default=False, verbose_name='Enable')),
                ('interval', models.CharField(blank=True, help_text='s/m/d', max_length=128, null=True, verbose_name='Interval')),
                ('crontab', models.CharField(blank=True, help_text='5 * * * *', max_length=128, null=True, verbose_name='Crontab')),
                ('meta', common.models.JsonDictTextField(blank=True, verbose_name='Meta')),
                ('execute_times', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_by', models.CharField(blank=True, max_length=128, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('plays', models.ManyToManyField(to='ansible_api.Play', verbose_name='Plays')),
            ],
        ),
        migrations.CreateModel(
            name='PlaybookExecution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('timedelta', models.FloatField(default=0.0, null=True, verbose_name='Time')),
                ('state', models.CharField(choices=[('PENDING', 'Pending'), ('STARTED', 'Started'), ('SUCCESS', 'Success'), ('FAILURE', 'Failure'), ('RETRY', 'Retry')], default='PENDING', max_length=16)),
                ('num', models.IntegerField(default=1)),
                ('result_summary', common.models.JsonDictTextField(blank=True, default='{}', null=True, verbose_name='Result summary')),
                ('result_raw', common.models.JsonDictTextField(blank=True, default='{}', null=True, verbose_name='Result raw')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('date_start', models.DateTimeField(null=True, verbose_name='Start time')),
                ('date_end', models.DateTimeField(null=True, verbose_name='End time')),
                ('playbook', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executions', to='ansible_api.Playbook')),
            ],
            options={
                'get_latest_by': 'date_start',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.SlugField(allow_unicode=True, max_length=128, unique=True, verbose_name='Name')),
                ('meta', common.models.JsonDictTextField(blank=True, null=True)),
                ('options', common.models.JsonCharField(blank=True, max_length=1024, null=True, verbose_name='Run options')),
                ('comment', models.CharField(blank=True, max_length=128, null=True, verbose_name='Comment')),
                ('created_by', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(message='Enter a valid name consisting of Unicode letters, numbers, underscores, or hyphens, or dot', regex='^[a-zA-Z0-9_\\-\\.]+$')])),
                ('type', models.CharField(choices=[('galaxy', 'galaxy'), ('git', 'git'), ('http', 'http'), ('file', 'file')], default='galaxy', max_length=16)),
                ('comment', models.CharField(blank=True, max_length=1024, verbose_name='Comment')),
                ('galaxy_name', models.CharField(blank=True, max_length=128, null=True)),
                ('git', common.models.JsonDictCharField(default={'branch': 'master', 'repo': ''}, max_length=4096)),
                ('url', models.CharField(blank=True, max_length=1024, verbose_name='Url')),
                ('logo', models.ImageField(null=True, upload_to='logo', verbose_name='Logo')),
                ('categories', models.CharField(blank=True, max_length=256, verbose_name='Tags')),
                ('version', models.CharField(blank=True, default='master', max_length=1024)),
                ('state', models.CharField(choices=[('uninstalled', 'UnInstalled'), ('installed', 'Installed'), ('installing', 'Installing'), ('failed', 'Failed')], default='uninstalled', max_length=16)),
                ('meta', common.models.JsonDictTextField(blank=True, verbose_name='Meta')),
                ('meta_ext', common.models.JsonDictTextField(blank=True, verbose_name='Meta Ext')),
                ('created_by', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project')),
            ],
        ),
        migrations.AddField(
            model_name='playbookexecution',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='playbook',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='play',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='host',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='group',
            name='hosts',
            field=models.ManyToManyField(related_name='groups', to='ansible_api.Host'),
        ),
        migrations.AddField(
            model_name='group',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='clusterhost',
            name='projects',
            field=models.ManyToManyField(related_name='cluster_hosts', to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='clustergroup',
            name='hosts',
            field=models.ManyToManyField(related_name='groups', to='ansible_api.ClusterHost'),
        ),
        migrations.AddField(
            model_name='clustergroup',
            name='projects',
            field=models.ManyToManyField(related_name='cluster_groups', to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='adhocexecution',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project'),
        ),
        migrations.AddField(
            model_name='adhoc',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ansible_api.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('name', 'project')},
        ),
        migrations.AlterUniqueTogether(
            name='playbook',
            unique_together={('name', 'project')},
        ),
        migrations.AlterUniqueTogether(
            name='host',
            unique_together={('name', 'project')},
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together={('name', 'project')},
        ),
        migrations.AlterUniqueTogether(
            name='clusterhost',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='clustergroup',
            unique_together={('name',)},
        ),
    ]
