# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.CharField(max_length=255, verbose_name='Slug')),
                ('prefix', models.CharField(help_text='The path to the html and rules.xml file.', max_length=255, verbose_name='Prefix', blank=True)),
                ('enabled', models.BooleanField(default=False, help_text='Enable this theme.', verbose_name='Enabled')),
                ('debug', models.BooleanField(default=False, help_text='Reload theme on every request (vs. reload on changing themes).', verbose_name='Debug')),
                ('pattern', models.CharField(default=b'.*', help_text='Select this theme when this pattern matches the requested url.', max_length=255, verbose_name='Pattern')),
                ('sort', models.IntegerField(help_text='The order in which the themes will be loaded (the lower, the earlier).', null=True, verbose_name='sort', blank=True)),
                ('path', models.CharField(max_length=255, null=True, verbose_name='Path', blank=True)),
                ('url', models.CharField(max_length=255, null=True, verbose_name='Url', blank=True)),
                ('builtin', models.BooleanField(default=False, verbose_name='Built-in')),
            ],
            options={
                'ordering': ('sort',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThemeUserAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(help_text='When pattern exists in HTTP_USER_AGENT', max_length=255, verbose_name='Pattern')),
                ('allow', models.CharField(help_text='Allow or deny loading this theme when the pattern matches.', max_length=10, verbose_name='Allow or deny', choices=[(b'allow', 'Allow'), (b'deny', 'Deny')])),
                ('sort', models.IntegerField(help_text='The order in which the patterns will be matched (the lower, the earlier).', null=True, verbose_name='sort', blank=True)),
                ('theme', models.ForeignKey(related_name='useragent_strings', to='django_diazo.Theme')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
