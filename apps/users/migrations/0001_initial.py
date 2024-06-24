# Generated by Django 4.1.13 on 2024-05-09 03:16

import uuid

import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, models

import common.db.fields
import common.db.models
import common.utils.django
import users.models.user


def add_default_group(apps, schema_editor):
    group_model = apps.get_model("users", "UserGroup")
    db_alias = schema_editor.connection.alias
    group_model.objects.using(db_alias).create(
        name="Default"
    )


def add_default_admin(apps, schema_editor):
    user_model = apps.get_model("users", "User")
    db_alias = schema_editor.connection.alias
    admin = user_model.objects.using(db_alias).create(
        username="admin", name="Administrator",
        email="admin@example.com", role="Admin",
        password=make_password("ChangeMe"),
    )
    group_model = apps.get_model("users", "UserGroup")
    default_group = group_model.objects.using(db_alias).get(name="Default")
    admin.groups.add(default_group)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128, unique=True, verbose_name='Username')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='Email')),
                ('role', models.CharField(blank=True, default='User', max_length=10, verbose_name='Role')),
                ('is_service_account', models.BooleanField(default=False, verbose_name='Is service account')),
                ('avatar', models.ImageField(null=True, upload_to='avatar', verbose_name='Avatar')),
                ('wechat', common.db.fields.EncryptCharField(blank=True, max_length=128, verbose_name='Wechat')),
                ('phone', common.db.fields.EncryptCharField(blank=True, max_length=128, null=True, verbose_name='Phone')),
                ('mfa_level', models.SmallIntegerField(choices=[(0, "Disabled"), (1, "Enabled"), (2, "Force enabled")], default=0, verbose_name='MFA')),
                ('otp_secret_key', common.db.fields.EncryptCharField(blank=True, max_length=128, null=True, verbose_name='OTP secret key')),
                ('private_key', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Private key')),
                ('public_key', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Public key')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('is_first_login', models.BooleanField(default=True, verbose_name='Is first login')),
                ('date_expired', models.DateTimeField(blank=True, db_index=True, default=common.utils.django.date_expired_default, null=True, verbose_name='Date expired')),
                ('created_by', models.CharField(blank=True, default='', max_length=30, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, default='', max_length=30, verbose_name='Updated by')),
                ('date_password_last_updated', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date password last updated')),
                ('need_update_password', models.BooleanField(default=False, verbose_name='Need update password')),
                ('source', models.CharField(choices=[('local', 'Local'), ('ldap', 'LDAP/AD'), ('openid', 'OpenID'), ('radius', 'Radius'), ('cas', 'CAS'), ('saml2', 'SAML2'), ('oauth2', 'OAuth2'), ('wecom', 'WeCom'), ('dingtalk', 'DingTalk'), ('feishu', 'FeiShu'), ('lark', 'Lark'), ('slack', 'Slack'), ('custom', 'Custom')], default='local', max_length=30, verbose_name='Source')),
                ('wecom_id', models.CharField(default=None, max_length=128, null=True, verbose_name='WeCom')),
                ('dingtalk_id', models.CharField(default=None, max_length=128, null=True, verbose_name='DingTalk')),
                ('feishu_id', models.CharField(default=None, max_length=128, null=True, verbose_name='FeiShu')),
                ('lark_id', models.CharField(default=None, max_length=128, null=True, verbose_name='Lark')),
                ('slack_id', models.CharField(default=None, max_length=128, null=True, verbose_name='Slack')),
                ('date_api_key_last_used', models.DateTimeField(blank=True, null=True, verbose_name='Date api key used')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
            ],
            options={
                'verbose_name': 'User',
                'ordering': ['username'],
                'permissions': [('invite_user', 'Can invite user'), ('remove_user', 'Can remove user'), ('match_user', 'Can match user')],
            },
            bases=(users.models.user.AuthMixin, users.models.user.SourceMixin, users.models.user.TokenMixin, users.models.user.RoleMixin, users.models.user.MFAMixin, users.models.user.JSONFilterMixin, models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserPasswordHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('user', models.ForeignKey(on_delete=common.db.models.CASCADE_SIGNAL_SKIP, related_name='history_passwords', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User password history',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'User group',
                'ordering': ['name'],
                'unique_together': {('org_id', 'name')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='users', to='users.usergroup', verbose_name='User group'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('category', models.CharField(max_length=128, verbose_name='Category')),
                ('value', models.TextField(blank=True, null=True, verbose_name='Value')),
                ('encrypted', models.BooleanField(default=False, verbose_name='Encrypted')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL, verbose_name='Users')),
            ],
            options={
                'verbose_name': 'Preference',
                'db_table': 'users_preference',
                'unique_together': {('name', 'user_id')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('dingtalk_id',), ('feishu_id',), ('wecom_id',), ('lark_id',), ('slack_id',)},
        ),
        migrations.RunPython(add_default_group),
        migrations.RunPython(add_default_admin),
    ]
