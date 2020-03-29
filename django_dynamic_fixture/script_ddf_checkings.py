import csv

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

def yellow(string):
    return color('93', string)


def ddf_check_models(application_labels=[], exclude_application_labels=[], print_csv=False, csv_filename=None):
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

    console_report(succeeded, errors)
    if print_csv or csv_filename:
        content = csv_report(succeeded, errors)
        if print_csv:
            print(yellow('\nCSV Report.\n'))
            print(content)
        if csv_filename:
            print(yellow('\nCSV Report file created: {}.\n'.format(csv_filename)))
            save_csv(content, filename=csv_filename)
    return succeeded, errors


def console_report(succeeded, errors):
    print(green('\nModels that DDF can create using the default settings.\n'))
    for i, (ref, _) in enumerate(succeeded.items(), start=1):
        i = str(i).zfill(3)
        print(white('{}. {}: '.format(i, ref)) + green('succeeded'))

    print(red('\nModels that requires some customisation.\n'))
    for i, (ref, error) in enumerate(errors.items(), start=1):
        i = str(i).zfill(3)
        print(white('{}. {}: '.format(i, ref)) + red(error))


def csv_report(succeeded, errors):
    SEP = '\t'
    LN = '\n'
    lines = []
    lines.append(SEP.join(['#', 'Model', 'Succeeded']))
    for i, (ref, _) in enumerate(succeeded.items(), start=1):
        lines.append(SEP.join([str(i), ref, 'succeeded']))

    lines.append(SEP.join(['#', 'Model', 'Error']))
    for i, (ref, error) in enumerate(errors.items(), start=1):
        lines.append(SEP.join([str(i), ref, error]))
    return LN.join(lines)


def save_csv(content, filename):
    with open(filename, 'w') as f:
        f.write(content)
