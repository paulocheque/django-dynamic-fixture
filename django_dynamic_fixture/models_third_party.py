from django.db import models


try:
    from django.contrib.postgres.fields import JSONField
    class ModelForPostgresFields(models.Model):
        nullable_json_field = JSONField(null=True)
        json_field = JSONField(null=False)
        class Meta:
            app_label = 'django_dynamic_fixture'
except ImportError:
    pass

try:
    from jsonfield import JSONField
    from jsonfield import JSONCharField
    class ModelForPlugins1(models.Model):
        json_field1 = JSONCharField(max_length=10)
        json_field2 = JSONField()
        class Meta:
            app_label = 'django_dynamic_fixture'
except ImportError:
    print('Library `jsonfield` not installed. Skipping.')


try:
    from json_field import JSONField as JSONField2
    class ModelForPlugins2(models.Model):
        json_field1 = JSONField2()
        class Meta:
            app_label = 'django_dynamic_fixture'
except ImportError:
    print('Library `django-json-field` not installed. Skipping.')


try:
    from polymorphic.models import PolymorphicModel
    class ModelPolymorphic(PolymorphicModel):
        class Meta:
            verbose_name = 'Polymorphic Model'


    class ModelPolymorphic2(ModelPolymorphic):
        class Meta:
            verbose_name = 'Polymorphic Model 2'


    class ModelPolymorphic3(ModelPolymorphic):
        class CannotSave(Exception):
            pass

        def save(self):
            raise self.CannotSave
except ImportError:
    print('Library `django_polymorphic` not installed. Skipping.')
