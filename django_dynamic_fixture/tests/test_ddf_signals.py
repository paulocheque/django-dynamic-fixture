# -*- coding: utf-8 -*-
from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.ddf import _PRE_SAVE, _POST_SAVE
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture


data_fixture = SequentialDataFixture()


class DDFTestCase(TestCase):
    def setUp(self):
        self.ddf = DynamicFixture(data_fixture)
        _PRE_SAVE.clear()
        _POST_SAVE.clear()



class PreSaveTest(DDFTestCase):
    def test_set_pre_save_receiver(self):
        def callback_function(instance):
            pass
        set_pre_save_receiver(ModelForSignals, callback_function)
        callback_function = lambda x: x
        set_pre_save_receiver(ModelForSignals, callback_function)

    def test_pre_save_receiver_must_raise_an_error_if_first_parameter_is_not_a_model_class(self):
        callback_function = lambda x: x
        with pytest.raises(InvalidReceiverError):
            set_pre_save_receiver(str, callback_function)

    def test_pre_save_receiver_must_raise_an_error_if_it_is_not_a_function(self):
        with pytest.raises(InvalidReceiverError):
            set_pre_save_receiver(ModelForSignals, '')

    def test_pre_save_receiver_must_raise_an_error_if_it_is_not_an_only_one_argument_function(self):
        callback_function = lambda x, y: x
        with pytest.raises(InvalidReceiverError):
            set_pre_save_receiver(ModelForSignals, callback_function)

    def test_pre_save_receiver_must_be_executed_before_saving(self):
        def callback_function(instance):
            if instance.id is not None:
                raise Exception('ops, instance already saved')
            self.ddf.get(ModelForSignals2)
        set_pre_save_receiver(ModelForSignals, callback_function)
        self.ddf.get(ModelForSignals)
        assert ModelForSignals2.objects.count() == 1

    def test_bugged_pre_save_receiver_must_raise_an_error(self):
        def callback_function(instance):
            raise Exception('ops')
        set_pre_save_receiver(ModelForSignals, callback_function)
        with pytest.raises(BadDataError):
            self.ddf.get(ModelForSignals)


class PostSaveTest(DDFTestCase):
    def test_set_post_save_receiver(self):
        def callback_function(instance):
            pass
        set_post_save_receiver(ModelForSignals, callback_function)
        callback_function = lambda x: x
        set_post_save_receiver(ModelForSignals, callback_function)

    def test_post_save_receiver_must_raise_an_error_if_first_parameter_is_not_a_model_class(self):
        callback_function = lambda x: x
        with pytest.raises(InvalidReceiverError):
            set_post_save_receiver(str, callback_function)

    def test_post_save_receiver_must_raise_an_error_if_it_is_not_a_function(self):
        with pytest.raises(InvalidReceiverError):
            set_post_save_receiver(ModelForSignals, '')

    def test_post_save_receiver_must_raise_an_error_if_it_is_not_an_only_one_argument_function(self):
        callback_function = lambda x, y: x
        with pytest.raises(InvalidReceiverError):
            set_post_save_receiver(ModelForSignals, callback_function)

    def test_pre_save_receiver_must_be_executed_before_saving(self):
        def callback_function(instance):
            if instance.id is None:
                raise Exception('ops, instance not saved')
            self.ddf.get(ModelForSignals2)
        set_post_save_receiver(ModelForSignals, callback_function)
        self.ddf.get(ModelForSignals)
        assert ModelForSignals2.objects.count() == 1

    def test_bugged_post_save_receiver_must_raise_an_error(self):
        def callback_function(instance):
            raise Exception('ops')
        set_post_save_receiver(ModelForSignals, callback_function)
        with pytest.raises(BadDataError):
            self.ddf.get(ModelForSignals)
