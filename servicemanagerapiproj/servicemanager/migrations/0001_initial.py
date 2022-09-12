# Generated by Django 4.1.1 on 2022-09-12 08:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdeaID', models.IntegerField()),
                ('Name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlatformID', models.IntegerField()),
                ('Name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StationID', models.IntegerField()),
                ('Name', models.CharField(max_length=250)),
                ('Desc', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Station', models.CharField(max_length=250, null=True)),
                ('IsDebugMode', models.BooleanField(default=b'I00\n')),
                ('RegressionName', models.CharField(max_length=250)),
                ('Tool', models.CharField(max_length=250, null=True)),
                ('ToolEvent', models.CharField(max_length=500, null=True)),
                ('ToolCounter', models.CharField(max_length=500, null=True)),
                ('Platform', models.CharField(max_length=500, null=True)),
                ('IsEmon', models.BooleanField(default=False)),
                ('PlatformEvent', models.CharField(max_length=500, null=True)),
                ('PlatformCounter', models.CharField(max_length=500, null=True)),
                ('Idea', models.CharField(max_length=500, null=True)),
                ('IsUploadResults', models.BooleanField(default=False)),
                ('TotalIterations', models.IntegerField(default=2)),
                ('Splitter', models.CharField(max_length=50)),
                ('MinImpurityDecrease', models.CharField(max_length=50)),
                ('MaxFeatures', models.CharField(max_length=50)),
                ('CreatedBy', models.CharField(max_length=50)),
                ('CreatedDate', models.DateTimeField()),
                ('ModifiedBy', models.CharField(max_length=50, null=True)),
                ('ModifiedDate', models.DateTimeField(null=True)),
                ('ErrorCode', models.CharField(max_length=10, null=True)),
                ('ErrorMessage', models.CharField(max_length=500, null=True)),
                ('Status', models.CharField(default='PENDING', max_length=50, null=True)),
                ('GUID', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('CurrentIteration', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaskStatusID', models.IntegerField()),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('ToolID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ToolEvent',
            fields=[
                ('ToolEventID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
                ('Tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='toolevents', to='servicemanager.tool')),
            ],
        ),
        migrations.CreateModel(
            name='ToolCounter',
            fields=[
                ('ToolCounterID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
                ('ToolEvent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='toolcounterevents', to='servicemanager.toolevent')),
            ],
        ),
        migrations.CreateModel(
            name='EmonEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmonEventID', models.IntegerField()),
                ('Name', models.CharField(max_length=150)),
                ('Platform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emonevents', to='servicemanager.platform')),
            ],
        ),
        migrations.CreateModel(
            name='EmonCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmonCounterID', models.IntegerField()),
                ('Name', models.CharField(max_length=150)),
                ('EmonEvent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emoncounters', to='servicemanager.emonevent')),
            ],
        ),
    ]
