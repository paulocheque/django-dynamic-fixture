# -*- coding: utf-8 -*-

from django.test import TestCase

from django_dynamic_fixture.models_test import EmptyModel, ModelWithRelationships, ModelForLibrary
from django_dynamic_fixture import N, G, F, C, P, look_up_alias, PRE_SAVE, POST_SAVE


class NShortcutTest(TestCase):
    def test_shortcut_N(self):
        instance = N(EmptyModel)
        self.assertEquals(None, instance.id)


class GShortcutTest(TestCase):
    def test_shortcut_G(self):
        instance = G(EmptyModel)
        self.assertNotEquals(None, instance.id)


class PShortcutTest(TestCase):
    def test_accept_model_instance(self):
        P(N(EmptyModel))
        P(G(EmptyModel))

    def test_accepts_list(self):
        P([N(EmptyModel), G(EmptyModel)])

    def test_accepts_tuple(self):
        P((N(EmptyModel), G(EmptyModel)))

    def test_accepts_queryset(self):
        P(EmptyModel.objects.all())


class FShortcutTest(TestCase):
    def test_fk(self):
        instance = G(ModelWithRelationships, integer=1000, foreignkey=F(integer=1001))
        self.assertEquals(1000, instance.integer)
        self.assertEquals(1001, instance.foreignkey.integer)

    def test_self_fk(self):
        instance = G(ModelWithRelationships, integer=1000, selfforeignkey=F(integer=1001))
        self.assertEquals(1000, instance.integer)
        self.assertEquals(1001, instance.selfforeignkey.integer)

    def test_o2o(self):
        instance = G(ModelWithRelationships, integer=1000, onetoone=F(integer=1001))
        self.assertEquals(1000, instance.integer)
        self.assertEquals(1001, instance.onetoone.integer)

    def test_m2m_with_one_element(self):
        instance = G(ModelWithRelationships, integer=1000, manytomany=[F(integer=1001)])
        self.assertEquals(1000, instance.integer)
        self.assertEquals(1001, instance.manytomany.all()[0].integer)

    def test_m2m_with_many_elements(self):
        instance = G(ModelWithRelationships, integer=1000, manytomany=[F(integer=1001), F(integer=1002)])
        self.assertEquals(1000, instance.integer)
        self.assertEquals(1001, instance.manytomany.all()[0].integer)
        self.assertEquals(1002, instance.manytomany.all()[1].integer)

    def test_full_example(self):
        instance = G(ModelWithRelationships, integer=1000,
                     foreignkey=F(integer=1001),
                     selfforeignkey=F(integer=1002),
                     onetoone=F(integer=1003),
                     manytomany=[F(integer=1004), F(integer=1005), F(selfforeignkey=F(integer=1006))])
        self.assertEquals(1000, instance.integer)
        self.assertEquals(1001, instance.foreignkey.integer)
        self.assertEquals(1002, instance.selfforeignkey.integer)
        self.assertEquals(1003, instance.onetoone.integer)
        self.assertEquals(1004, instance.manytomany.all()[0].integer)
        self.assertEquals(1005, instance.manytomany.all()[1].integer)
        self.assertEquals(1006, instance.manytomany.all()[2].selfforeignkey.integer)

    def test_using_look_up_alias(self):
        instance = G(ModelWithRelationships, integer=1000,
                     foreignkey__integer=1001,
                     selfforeignkey__integer=1002,
                     onetoone__integer=1003,
                     manytomany=[F(integer=1004), F(integer=1005), F(selfforeignkey__integer=1006)])
        self.assertEquals(1000, instance.integer)
        self.assertEquals(1001, instance.foreignkey.integer)
        self.assertEquals(1002, instance.selfforeignkey.integer)
        self.assertEquals(1003, instance.onetoone.integer)
        self.assertEquals(1004, instance.manytomany.all()[0].integer)
        self.assertEquals(1005, instance.manytomany.all()[1].integer)
        self.assertEquals(1006, instance.manytomany.all()[2].selfforeignkey.integer)


class CShortcutTest(TestCase):
    def test_copying_from_the_same_model(self):
        instance = G(ModelWithRelationships, integer=C('integer_b'))
        self.assertEquals(instance.integer, instance.integer_b)

    def test_copying_from_a_fk(self):
        instance = G(ModelWithRelationships, integer=C('foreignkey.integer'))
        self.assertEquals(instance.integer, instance.foreignkey.integer)

    def test_copying_from_a_one2one(self):
        instance = G(ModelWithRelationships, integer=C('onetoone.integer'))
        self.assertEquals(instance.integer, instance.onetoone.integer)

    def test_copying_from_a_self_fk(self):
        instance = G(ModelWithRelationships, integer=C('selfforeignkey.integer_b'))
        self.assertEquals(instance.integer, instance.selfforeignkey.integer_b)

    def test_copying_inside_fk(self):
        instance = G(ModelWithRelationships, selfforeignkey=F(integer=C('selfforeignkey.integer_b')))
        self.assertEquals(instance.selfforeignkey.integer, instance.selfforeignkey.selfforeignkey.integer_b)

    def test_copying_inside_many_to_many(self):
        instance = G(ModelWithRelationships, manytomany=[F(integer=C('integer_b'))])
        instance1 = instance.manytomany.all()[0]
        self.assertEquals(instance1.integer, instance1.integer_b)


class ShelveAndLibraryTest(TestCase):
    def test_shelve(self):
        instance = G(ModelForLibrary, integer=1000, shelve=True)
        self.assertEquals(1000, instance.integer)

        instance = G(ModelForLibrary, use_library=False)
        self.assertNotEquals(1000, instance.integer)

        instance = G(ModelForLibrary, use_library=True)
        self.assertEquals(1000, instance.integer)

        instance = G(ModelForLibrary, integer=1001, use_library=True)
        self.assertEquals(1001, instance.integer)


class CreatingMultipleObjectsTest(TestCase):
    def test_new(self):
        self.assertEquals([], N(EmptyModel, n=0))
        self.assertEquals([], N(EmptyModel, n= -1))
        self.assertTrue(isinstance(N(EmptyModel), EmptyModel)) # default is 1
        self.assertTrue(isinstance(N(EmptyModel, n=1), EmptyModel))
        self.assertEquals(2, len(N(EmptyModel, n=2)))

    def test_get(self):
        self.assertEquals([], G(EmptyModel, n=0))
        self.assertEquals([], G(EmptyModel, n= -1))
        self.assertTrue(isinstance(G(EmptyModel), EmptyModel)) # default is 1
        self.assertTrue(isinstance(G(EmptyModel, n=1), EmptyModel))
        self.assertEquals(2, len(G(EmptyModel, n=2)))


class LookUpSeparatorTest(TestCase):
    def test_look_up_alias_with_just_one_parameter(self):
        self.assertEquals({'a': 1}, look_up_alias(a=1))
        self.assertEquals({'a': F()}, look_up_alias(a=F()))
        self.assertEquals({'a_b': 1}, look_up_alias(a_b=1))
        self.assertEquals({'a': F(b=1)}, look_up_alias(a__b=1))
        self.assertEquals({'a_b': F(c=1)}, look_up_alias(a_b__c=1))
        self.assertEquals({'a': F(b=F(c=1))}, look_up_alias(a__b__c=1))
        self.assertEquals({'a_b': F(c_d=F(e_f=1))}, look_up_alias(a_b__c_d__e_f=1))

    def test_look_up_alias_with_many_parameters(self):
        self.assertEquals({'a': 1, 'b': 2}, look_up_alias(a=1, b=2))
        self.assertEquals({'a': 1, 'b_c': 2}, look_up_alias(a=1, b_c=2))
        self.assertEquals({'a': 1, 'b': F(c=2)}, look_up_alias(a=1, b__c=2))
        self.assertEquals({'a': F(b=1), 'c': F(d=2)}, look_up_alias(a__b=1, c__d=2))


class PreAndPostSaveTest(TestCase):
    def test_pre_save(self):
        PRE_SAVE(EmptyModel, lambda x: x)

    def test_post_save(self):
        POST_SAVE(EmptyModel, lambda x: x)

