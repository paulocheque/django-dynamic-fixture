#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_dynamic_fixture.django_helper import django_greater_than


class EmptyModel(models.Model):
    pass


class ModelWithNumbers(models.Model):
    #id is a models.AutoField()
    integer = models.IntegerField(null=True, unique=True)
    smallinteger = models.SmallIntegerField(null=True, unique=True)
    positiveinteger = models.PositiveIntegerField(null=True, unique=True)
    positivesmallinteger = models.PositiveSmallIntegerField(null=True, unique=True)
    biginteger = models.BigIntegerField(null=True, unique=True)
    float = models.FloatField(null=True, unique=True)
    decimal = models.DecimalField(max_digits=2, decimal_places=1, null=True, unique=False)

    class Meta:
        verbose_name = 'Numbers'


class ModelWithStrings(models.Model):
    string = models.CharField(max_length=1, null=True, unique=True)
    text = models.TextField(null=True, unique=True)
    slug = models.SlugField(null=True, unique=True)
    commaseparated = models.CommaSeparatedIntegerField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = 'Strings'


class ModelWithBooleans(models.Model):
    # https://docs.djangoproject.com/en/1.6/ref/models/fields/#booleanfield
    # Django 1.6 changed the default value of BooleanField from False to None
    boolean = models.BooleanField()
    nullboolean = models.NullBooleanField()

    class Meta:
        verbose_name = 'Booleans'


class ModelWithDateTimes(models.Model):
    date = models.DateField(null=True, unique=True)
    datetime = models.DateTimeField(null=True, unique=True)
    time = models.TimeField(null=True, unique=True)

    class Meta:
        verbose_name = 'DateTimes'


if django_greater_than('1.6'):
    class ModelWithBinary(models.Model):
        binary = models.BinaryField()

class ModelWithFieldsWithCustomValidation(models.Model):
    email = models.EmailField(null=True, unique=True)
    url = models.URLField(null=True, unique=True)
    ip = models.IPAddressField(null=True, unique=False)
    if django_greater_than('1.4'):
        ipv6 = models.GenericIPAddressField(null=True, unique=False)

    class Meta:
        verbose_name = 'Custom validation'


class ModelWithFileFields(models.Model):
    filepath = models.FilePathField(unique=True, blank=True)
    file = models.FileField(upload_to='.')

    try:
        import pil
        # just test it if the PIL package is installed
        image = models.ImageField(upload_to='.')
    except ImportError:
        pass

    class Meta:
        verbose_name = 'File fields'


class ModelWithDefaultValues(models.Model):
    integer_with_default = models.IntegerField(null=True, default=3)
    string_with_choices = models.CharField(max_length=5, null=True, choices=(('a', 'A'), ('b', 'B')))
    string_with_choices_and_default = models.CharField(max_length=5, null=True, default='b', choices=(('a', 'A'), ('b', 'B')))
    string_with_optgroup_choices = models.CharField(max_length=5, null=True, choices=(('group1', (('a', 'A'), ('b', 'B'))), ('group2', (('c', 'C'), ('d', 'D')))))
    foreign_key_with_default = models.ForeignKey(EmptyModel, null=True, default=None)

    class Meta:
        verbose_name = 'Default values'


class ModelForNullable(models.Model):
    nullable = models.IntegerField(null=True)
    not_nullable = models.IntegerField(null=False)

    class Meta:
        verbose_name = 'Nullable'


class ModelForIgnoreList2(models.Model):
    nullable = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Ignore list 2'


class ModelForIgnoreList(models.Model):
    required = models.IntegerField(null=False)
    required_with_default = models.IntegerField(null=False, default=1)
    not_required = models.IntegerField(null=True)
    not_required_with_default = models.IntegerField(null=True, default=1)
    self_reference = models.ForeignKey('ModelForIgnoreList', null=True)
    different_reference = models.ForeignKey(ModelForIgnoreList2, null=True)

    class Meta:
        verbose_name = 'Ignore list'


class ModelRelated(models.Model):
    selfforeignkey = models.ForeignKey('self', null=True)
    integer = models.IntegerField(null=True)
    integer_b = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Related'


class ModelRelatedThrough(models.Model):
    related = models.ForeignKey('ModelRelated')
    relationship = models.ForeignKey('ModelWithRelationships')


def default_fk_value():
    try:
        return ModelRelated.objects.get(id=1)
    except ModelRelated.DoesNotExist:
        ModelRelated.objects.create()
        return ModelRelated.objects.all()[0]


def default_fk_id():
    return default_fk_value().pk


class ModelWithRelationships(models.Model):
    # relationship
    selfforeignkey = models.ForeignKey('self', null=True)
    foreignkey = models.ForeignKey('ModelRelated', related_name='fk', null=True)
    onetoone = models.OneToOneField('ModelRelated', related_name='o2o', null=True)
    manytomany = models.ManyToManyField('ModelRelated', related_name='m2m')
    manytomany_through = models.ManyToManyField('ModelRelated', related_name='m2m_through', through=ModelRelatedThrough)

    foreignkey_with_default = models.ForeignKey('ModelRelated', related_name='fk2', null=True, default=default_fk_value)
    foreignkey_with_id_default = models.ForeignKey('ModelRelated', related_name='fk3', null=True, default=default_fk_id)

    integer = models.IntegerField(null=True)
    integer_b = models.IntegerField(null=True)
    # generic field
    # TODO

    class Meta:
        verbose_name = 'Relationships'


class ModelWithCyclicDependency(models.Model):
    d = models.ForeignKey('ModelWithCyclicDependency2', null=True)

    class Meta:
        verbose_name = 'Cyclic dependency'


class ModelWithCyclicDependency2(models.Model):
    c = models.ForeignKey(ModelWithCyclicDependency, null=True)

    class Meta:
        verbose_name = 'Cyclic dependency 2'


class ModelAbstract(models.Model):
    integer = models.IntegerField(null=True, unique=True)
    class Meta:
        abstract = True
        verbose_name = 'Abstract'


class ModelParent(ModelAbstract):
    class Meta:
        verbose_name = 'Parent'


class ModelChild(ModelParent):
    class Meta:
        verbose_name = 'Child'


class ModelChildWithCustomParentLink(ModelParent):
    my_custom_ref = models.OneToOneField(ModelParent, parent_link=True, related_name='my_custom_ref_x')

    class Meta:
        verbose_name = 'Custom child'


class ModelWithRefToParent(models.Model):
    parent = models.ForeignKey(ModelParent)

    class Meta:
        verbose_name = 'Child with parent'


class CustomDjangoField(models.IntegerField):
    pass


class CustomDjangoField2(models.IntegerField):
    pass


class CustomDjangoFieldMixin(object):
    pass


class CustomDjangoFieldMultipleInheritance(CustomDjangoFieldMixin, models.IntegerField):
    pass


class NewField(models.Field):
    pass


class ModelWithCustomFields(models.Model):
    x = CustomDjangoField(null=False)
    y = NewField(null=True)

    class Meta:
        verbose_name = 'Custom fields'


class ModelWithCustomFieldsMultipleInheritance(models.Model):
    x = CustomDjangoFieldMultipleInheritance(null=False)
    y = NewField(null=True)

    class Meta:
        verbose_name = 'Custom fields with multiple inheritance'


class ModelWithUnsupportedField(models.Model):
    z = NewField(null=False)

    class Meta:
        verbose_name = 'Unsupported field'


class ModelWithValidators(models.Model):
    field_validator = models.CharField(max_length=3, validators=[RegexValidator(regex=r'ok')])
    clean_validator = models.CharField(max_length=3)

    class Meta:
        verbose_name = 'Validators'

    def clean(self):
        if self.clean_validator != 'ok':
            raise ValidationError('ops')


class ModelWithAutoDateTimes(models.Model):
    auto_now_add = models.DateField(auto_now_add=True)
    auto_now = models.DateField(auto_now=True)
    manytomany = models.ManyToManyField('ModelWithAutoDateTimes', related_name='m2m')

    class Meta:
        verbose_name = 'Auto DateTime'


class ModelForCopy2(models.Model):
    int_e = models.IntegerField()

    class Meta:
        verbose_name = 'Copy 2'


class ModelForCopy(models.Model):
    int_a = models.IntegerField()
    int_b = models.IntegerField(null=None)
    int_c = models.IntegerField()
    int_d = models.IntegerField()
    e = models.ForeignKey(ModelForCopy2)

    class Meta:
        verbose_name = 'Copy'


class ModelForLibrary2(models.Model):
    integer = models.IntegerField(null=True)
    integer_unique = models.IntegerField(null=True, unique=True)

    class Meta:
        verbose_name = 'Library 2'


class ModelForLibrary(models.Model):
    integer = models.IntegerField(null=True)
    integer_unique = models.IntegerField(null=True, unique=True)
    selfforeignkey = models.ForeignKey('self', null=True)
    foreignkey = models.ForeignKey('ModelForLibrary2', related_name='fk', null=True)

    class Meta:
        verbose_name = 'Library'


class ModelForDDFSetup(models.Model):
    integer = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'DDF setup'


class ModelWithClean(models.Model):
    integer = models.IntegerField()

    class Meta:
        verbose_name = 'Clean'

    def clean(self):
        if self.integer != 9999: # just for testing
            raise ValidationError('integer is not 9999')


class ModelForSignals(models.Model):
    class Meta:
        verbose_name = 'Signals'


class ModelForSignals2(models.Model):
    class Meta:
        verbose_name = 'Signals 2'


class ModelForFieldPlugins(models.Model):
    # aaa = CustomDjangoField(null=False) # defined in settings.py
    # bbb = models.IntegerField(null=False)
    custom_field_custom_fixture = CustomDjangoField(null=False) # defined in settings.py
    custom_field_custom_fixture2 = CustomDjangoField2(null=False) # defined in settings.py


class ModelWithCommonNames(models.Model):
    instance = models.IntegerField(null=False)
    field = models.IntegerField(null=False)


# GeoDjango requires Django 1.7+
if django_greater_than('1.7') and settings.DDF_TEST_GEODJANGO:
    from django.contrib.gis.db import models as geomodels
    class ModelForGeoDjango(geomodels.Model):
        geometry = geomodels.GeometryField()
        point = geomodels.PointField()
        line_string = geomodels.LineStringField()
        polygon = geomodels.PolygonField()
        multi_point = geomodels.MultiPointField()
        multi_line_string = geomodels.MultiLineStringField()
        multi_polygon = geomodels.MultiPolygonField()
        geometry_collection = geomodels.GeometryCollectionField()


if django_greater_than('1.8'):
    class ModelForUUID(models.Model):
        uuid = models.UUIDField()


# jsonfield requires Django 1.4+
if django_greater_than('1.4'):
    try:
        from jsonfield import JSONField
        from jsonfield import JSONCharField
        class ModelForPlugins1(models.Model):
            json_field1 = JSONCharField(max_length=10)
            json_field2 = JSONField()
    except ImportError:
        pass


try:
    from json_field import JSONField as JSONField2
    class ModelForPlugins2(models.Model):
        json_field1 = JSONField2()
except ImportError:
    pass
