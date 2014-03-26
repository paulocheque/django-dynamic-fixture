# -*- coding: utf-8 -*-

import os
import tempfile

from shutil import rmtree, copy2
from django.core.files import File

from django.test import TestCase
from django.conf import settings
from django.core.files.storage import FileSystemStorage


TEMP_PATH = tempfile.gettempdir() or os.environ.get('TEMP')
TEMP_PATH_DDF = os.path.join(TEMP_PATH, 'DDF_TEMP')


class CustomFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super(CustomFileSystemStorage, self).\
        __init__(location=TEMP_PATH_DDF, *args, **kwargs)


class FileSystemDjangoTestCase(TestCase):
    TEAR_DOWN_ENABLED = True

    def setUp(self):
        self.fdf_setup()

    def tearDown(self):
        self.fdf_teardown()

    def _pre_setup(self):
        super(FileSystemDjangoTestCase, self)._pre_setup()
        self.fdf_setup()

    def _post_teardown(self):
        "Try to remove all files and directories created by the test."
        super(FileSystemDjangoTestCase, self)._post_teardown()
        self.fdf_teardown()

    def fdf_setup(self):
        self.directories = []
        self.files = {}
        setattr(settings, 'DEFAULT_FILE_STORAGE', 'django_dynamic_fixture.fdf.CustomFileSystemStorage')

    def fdf_teardown(self):
        if self.TEAR_DOWN_ENABLED:
            while self.files:
                self.remove_temp_file(next(iter(self.files.keys())))
            while self.directories:
                self.remove_temp_directory(self.directories[0])
            if os.path.exists(TEMP_PATH_DDF):
                rmtree(TEMP_PATH_DDF)

    def create_temp_directory(self, prefix='file_system_test_case_dir_'):
        "Create a temporary directory and returns the directory pathname."
        directory = tempfile.mkdtemp(prefix=prefix)
        self.directories.append(directory)
        return directory

    def remove_temp_directory(self, directory_pathname):
        "Remove a directory."
        rmtree(directory_pathname)
        if directory_pathname in self.directories:
            try:
                self.directories.remove(directory_pathname)
            except WindowsError:
                pass

    def create_temp_file(self, directory=None, prefix='file_system_test_case_file_', suffix='.tmp'):
        """
        Create a temporary file with a option prefix and suffix in a temporary or custom directory.
        Returns the filepath
        """
        tmp_file = tempfile.mkstemp(prefix=prefix, dir=directory, suffix=suffix)
        file_obj = os.fdopen(tmp_file[0])
        self.files[tmp_file[1]] = file_obj
        return tmp_file[1]

    def create_temp_file_with_name(self, directory, name):
        "Create a temporary file with a specified name."
        filepath = os.path.join(directory, name)
        file_obj = open(filepath, 'wb')
        file_obj.close()
        self.files[filepath] = file_obj
        return filepath

    def rename_temp_file(self, filepath, name):
        "Rename an existent file. 'name' is not a file path, so it must not include the directory path name."
        directory = self.get_directory_of_the_file(filepath)
        new_filepath = os.path.join(directory, name)
        os.rename(filepath, new_filepath)
        if filepath in self.files.keys():
            self.files.pop(filepath)
        self.files[new_filepath] = open(new_filepath, 'a+b')
        self.files[new_filepath].close()
        return new_filepath

    def remove_temp_file(self, filepath):
        "Remove a file."
        if filepath in self.files.keys():
            fileobj = self.files.pop(filepath)
            fileobj.close()
        if os.path.exists(filepath):
            try:
                os.unlink(filepath)
            except WindowsError:
                pass

    def copy_file_to_dir(self, filepath, directory):
        "Copy a file to a specified directory."
        copy2(filepath, directory)
        return self.get_filepath(directory, self.get_filename(filepath))

    def add_text_to_file(self, filepath, content):
        "Add text to an existent file."
        file = open(filepath, 'a')
        file.write(content)
        file.close()

    def get_directory_of_the_file(self, filepath):
        "Get the directory path name of a file."
        return os.path.dirname(filepath)

    def get_filename(self, filepath):
        "Get the filename of a file."
        return os.path.basename(filepath)

    def get_filepath(self, directory, filename):
        "Get the file path of a file with a defined name in a directory."
        return os.path.join(directory, filename)

    def get_content_of_file(self, filepath):
        "Returns the content of a file."
        file = open(filepath, 'r')
        content = file.read()
        file.close()
        return content

    def create_django_file_with_temp_file(self, name, content=None, dir=None, prefix='file_system_test_case_file_', suffix='.tmp'):
        "Create and returns a django.core.files.File"
        file = open(self.create_temp_file(directory=dir, prefix=prefix, suffix=suffix), 'w')
        file.close()
        django_file = File(file, name=name)
        self.files[django_file.file.name] = open(django_file.file.name, 'a+b')
        if content:
            self.files[django_file.file.name].write(content)
        self.files[django_file.file.name].close()
        return django_file

    def create_django_file_using_file(self, filepath):
        "Create and returns a django.core.files.File"
        new_filepath = self.copy_file_to_dir(filepath, self.create_temp_directory())
        the_file = open(new_filepath, 'rb')
        django_file = File(the_file, name=os.path.basename(new_filepath))
        self.files[django_file.file.name] = the_file
        #self.files[django_file.file.name].close()
        return django_file

    def assertFileExists(self, filepath):
        self.assertTrue(os.path.exists(filepath), msg='%s does not exist' % filepath)

    def assertFileDoesNotExists(self, filepath):
        self.assertFalse(os.path.exists(filepath), msg='%s exist' % filepath)

    def assertDirectoryExists(self, directory):
        "@directory must be the directory path"
        self.assertTrue(os.path.exists(directory), msg='%s does not exist' % directory)

    def assertDirectoryDoesNotExists(self, directory):
        "@directory must be the directory path"
        self.assertFalse(os.path.exists(directory), msg='%s exist' % directory)

    def assertDirectoryContainsFile(self, directory, filename):
        filepath = os.path.join(directory, filename)
        self.assertFileExists(filepath)

    def assertDirectoryDoesNotContainsFile(self, directory, filename):
        filepath = os.path.join(directory, filename)
        self.assertFileDoesNotExists(filepath)

    def assertFilesHaveEqualLastModificationTimestamps(self, filepath1, filepath2):
        self.assertEquals(0, os.path.getmtime(filepath1) - os.path.getmtime(filepath2))

    def assertFilesHaveNotEqualLastModificationTimestamps(self, filepath1, filepath2):
        self.assertNotEquals(0, os.path.getmtime(filepath1) - os.path.getmtime(filepath2))

    def assertNumberOfFiles(self, directory, number_of_files):
        filenames = [filename for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
        self.assertEquals(number_of_files, len(filenames), msg='[%s] %s' % (len(filenames), filenames))
