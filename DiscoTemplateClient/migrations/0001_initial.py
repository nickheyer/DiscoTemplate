# Generated by Django 4.2.4 on 2023-10-25 06:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix_keyword', models.CharField(default='!dt', max_length=255, null=True, verbose_name='Chat-Prefix For Requests')),
                ('discord_token', models.CharField(default='', max_length=255, null=True, verbose_name='Discord Token')),
                ('session_timeout', models.IntegerField(default=60, null=True, verbose_name='Session Timeout')),
                ('is_verbose_logging', models.BooleanField(default=False, verbose_name='Verbose logging in console')),
                ('is_debug', models.BooleanField(default=False, verbose_name='Send Debug Message On Error')),
            ],
        ),
        migrations.CreateModel(
            name='DiscordServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(max_length=255, null=True)),
                ('server_id', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ErrLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('entry', models.CharField(default='Error Occured', max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('entry', models.CharField(default='Event Occured', max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_state', models.BooleanField(default=False)),
                ('app_state', models.BooleanField(default=True)),
                ('current_activity', models.CharField(default='Offline', max_length=255)),
                ('host_url', models.CharField(default='0.0.0.0:5454', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('added', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_server_restricted', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('is_additional_settings', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('session_timeout', models.IntegerField(default=60)),
                ('discord_servers', models.ManyToManyField(blank=True, related_name='users', to='DiscoTemplateClient.discordserver')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
