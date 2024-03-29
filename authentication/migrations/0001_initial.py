# Generated by Django 4.2 on 2023-04-13 10:57

import authentication.validators
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': "Ce nom d'utilisateur est déjà utilisé."}, help_text="Nom d'utilisateur composé de lettres, chiffres, -/_/. de 20 caractères maximum.", max_length=20, unique=True, validators=[django.core.validators.RegexValidator(code='invalid', message="Le nom d'utilisateur doit être composé de 4 à 20 caractères alphanumériques, des tirets, des underscores ou des points.", regex='^[a-zA-Z0-9_\\-.]{4,20}$')], verbose_name="nom d'utilisateur")),
                ('date_of_birth', models.DateField(validators=[authentication.validators.date_of_birth_validator], verbose_name='date de naissance')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='prénom')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='biographie')),
                ('email', models.EmailField(blank=True, help_text="L'adresse mail permet de récupérer son compte en cas de perte de mot de passe. Elle n'est pas publiée sur votre profil.", max_length=254, verbose_name='adresse mail')),
                ('study', models.CharField(blank=True, max_length=100, verbose_name='études (classe)')),
                ('instagram', models.CharField(blank=True, max_length=100, validators=[django.core.validators.RegexValidator(code='invalid', message="Le nom du d'utilisateur instagram ne correspond pas à la norme.", regex='^(?!.*\\.\\.)(?!.*\\.$)[^\\W][\\w.]{0,29}$')], verbose_name='instagram')),
                ('twitter', models.CharField(blank=True, max_length=100, validators=[django.core.validators.RegexValidator(code='invalid', message="Le nom du d'utilisateur twitter ne correspond pas à la norme.", regex='^[A-Za-z0-9_]{1,15}$')], verbose_name='twitter')),
                ('github', models.CharField(blank=True, max_length=100, verbose_name='github')),
                ('website', models.URLField(blank=True, verbose_name='site web')),
                ('is_staff', models.BooleanField(default=False, help_text="Permet de définir si l'utilisateur peut se connecter à l'administration.", verbose_name='membre du staff')),
                ('is_active', models.BooleanField(default=True, help_text="Permet de définir si l'utilisateur peut se connecter. Désactivez-le pour pour bannir un utilisateur ou désactiver un compte sans le supprimer.", verbose_name='actif')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name="date d'inscription")),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'utilisateur',
                'verbose_name_plural': 'utilisateurs',
                'permissions': (('edit_own_profile', 'Peut éditer son propre profil'), ('edit_profile', "Peut éditer le profil d'un utilisateur")),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('username'), name='unique_username'),
        ),
    ]
