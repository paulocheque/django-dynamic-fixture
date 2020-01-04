from django.db import transaction

from django_dynamic_fixture.django_helper import get_apps, get_models_of_an_app


def color(color, string):
    return '\033[1;{}m{}\033[0m'.format(color, string)

def white(string):
    return color('37', string)

def red(string):
    return color('91', string)

def green(string):
    return color('92', string)


def ddf_check_models(application_labels=[], exclude_application_labels=[]):
    from django_dynamic_fixture import get

    succeeded = {}
    errors = {}
    for app_label in get_apps(application_labels, exclude_application_labels):
        models = get_models_of_an_app(app_label)
        for model_class in models:
            ref = '{}.{}'.format(app_label, model_class.__name__)
            try:
                with transaction.atomic():
                    get(model_class)
                succeeded[ref] = None
            except Exception as e:
                errors[ref] = '[{}] {}'.format(type(e), str(e))

    # Print report
    print(green('\nModels that DDF can create using the default settings.\n'))
    for i, (ref, _) in enumerate(succeeded.items()):
        i = str(i).zfill(3)
        print(white('{}. {}: '.format(i, ref)) + green('succeeded'))

    print(red('\nModels that requires some customisation.\n'))
    for i, (ref, error) in enumerate(errors.items(), start=1):
        i = str(i).zfill(3)
        print(white('{}. {}: '.format(i, ref)) + red(error))

    return succeeded, errors
