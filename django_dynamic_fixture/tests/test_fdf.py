# -*- coding: utf-8 -*-

from tempfile import mkdtemp, mkstemp

from django_dynamic_fixture.fdf import *
from django.core.files import File


class FileSystemDjangoTestCaseDealWithDirectoriesTest(FileSystemDjangoTestCase):

    def test_create_temp_directory_must_create_an_empty_directory(self):
        directory = self.create_temp_directory()
        self.assertDirectoryExists(directory)
        self.assertNumberOfFiles(directory, 0)

    def test_remove_temp_directory(self):
        directory = self.create_temp_directory()
        self.remove_temp_directory(directory)
        self.assertDirectoryDoesNotExists(directory)

    def test_remove_temp_directory_must_remove_directories_created_out_of_the_testcase_too(self):
        directory = mkdtemp()
        self.remove_temp_directory(directory)
        self.assertDirectoryDoesNotExists(directory)

    def test_remove_temp_directory_must_remove_their_files_too(self):
        directory = self.create_temp_directory()
        self.create_temp_file_with_name(directory, 'x.txt')
        self.remove_temp_directory(directory)
        self.assertDirectoryDoesNotExists(directory)


class FileSystemDjangoTestCaseDealWithTemporaryFilesTest(FileSystemDjangoTestCase):

    def test_create_temp_file_must_create_a_temporary_file_in_an_arbitrary_directory(self):
        filepath = self.create_temp_file()
        self.assertFileExists(filepath)

        directory = self.get_directory_of_the_file(filepath)
        filename = self.get_filename(filepath)
        self.assertDirectoryContainsFile(directory, filename)

    def test_create_temp_file_must_create_an_empty_temporary_file(self):
        filepath = self.create_temp_file()
        self.assertEquals('', self.get_content_of_file(filepath))

    def test_create_temp_file_must_is_ready_to_add_content_to_it(self):
        filepath = self.create_temp_file()
        self.add_text_to_file(filepath, 'abc')
        self.assertEquals('abc', self.get_content_of_file(filepath))


class FileSystemDjangoTestCaseDealWithSpecificTemporaryFilesTest(FileSystemDjangoTestCase):

    def test_create_temp_file_with_name_must_create_a_file_in_an_specific_directory_with_an_specific_name(self):
        directory = self.create_temp_directory()
        filepath = self.create_temp_file_with_name(directory, 'x.txt')
        self.assertFileExists(filepath)

        self.assertEquals(directory, self.get_directory_of_the_file(filepath))
        self.assertEquals('x.txt', self.get_filename(filepath))
        self.assertDirectoryContainsFile(directory, self.get_filename(filepath))
        self.assertNumberOfFiles(directory, 1)

    def test_create_temp_file_with_name_must_create_an_empty_file(self):
        directory = self.create_temp_directory()
        filepath = self.create_temp_file_with_name(directory, 'x.txt')
        self.assertEquals('', self.get_content_of_file(filepath))

    def test_create_temp_file_with_name_is_ready_to_add_content_to_it(self):
        directory = self.create_temp_directory()
        filepath = self.create_temp_file_with_name(directory, 'x.txt')
        self.add_text_to_file(filepath, 'abc')
        self.assertEquals('abc', self.get_content_of_file(filepath))


class FileSystemDjangoTestCaseCanRenameFilesTest(FileSystemDjangoTestCase):

    def test_rename_file_must_preserve_the_directory(self):
        directory = self.create_temp_directory()
        old_filepath = self.create_temp_file_with_name(directory, 'x.txt')
        old_filename = self.get_filename(old_filepath)

        new_filepath = self.rename_temp_file(old_filepath, 'y.txt')
        self.assertFileExists(new_filepath)
        self.assertFileDoesNotExists(old_filepath)

        new_filename = self.get_filename(new_filepath)
        self.assertDirectoryContainsFile(directory, new_filename)
        self.assertDirectoryDoesNotContainsFile(directory, old_filename)

    def test_rename_file_must_preserve_the_file_content(self):
        directory = self.create_temp_directory()
        old_filepath = self.create_temp_file_with_name(directory, 'x.txt')
        self.add_text_to_file(old_filepath, 'abc')

        new_filepath = self.rename_temp_file(old_filepath, 'y.txt')

        self.assertEquals('abc', self.get_content_of_file(new_filepath))


class FileSystemDjangoTestCaseCanRemoveFilesTest(FileSystemDjangoTestCase):

    def test_remove_file(self):
        filepath = self.create_temp_file()
        self.remove_temp_file(filepath)
        self.assertFileDoesNotExists(filepath)

    def test_remove_file_must_remove_files_with_custom_name_too(self):
        directory = self.create_temp_directory()
        filepath = self.create_temp_file_with_name(directory, 'x.txt')
        self.remove_temp_file(filepath)
        self.assertFileDoesNotExists(filepath)

    def test_remove_file_must_remove_files_with_data_too(self):
        filepath = self.create_temp_file()
        self.add_text_to_file(filepath, 'abc')
        self.remove_temp_file(filepath)
        self.assertFileDoesNotExists(filepath)


class FileSystemDjangoTestCaseCanCopyFilesTest(FileSystemDjangoTestCase):

    def test_copy_file_to_dir_must_not_remove_original_file(self):
        directory = self.create_temp_directory()
        filepath = self.create_temp_file()

        new_filepath = self.copy_file_to_dir(filepath, directory)

        self.assertFileExists(new_filepath)
        self.assertFileExists(filepath)

    def test_copy_file_to_dir_must_preserve_file_content(self):
        directory = self.create_temp_directory()
        filepath = self.create_temp_file()
        self.add_text_to_file(filepath, 'abc')

        new_filepath = self.copy_file_to_dir(filepath, directory)
        self.assertEquals('abc', self.get_content_of_file(new_filepath))


class FileSystemDjangoTestCaseDealWithDjangoFileFieldTest(FileSystemDjangoTestCase):

    def test_django_file_must_create_a_django_file_object(self):
        django_file = self.create_django_file_with_temp_file('x.txt')
        self.assertTrue(isinstance(django_file, File))
        self.assertEquals('x.txt', django_file.name)

    def test_django_file_must_create_a_temporary_file_ready_to_add_content(self):
        django_file = self.create_django_file_with_temp_file('x.txt')
        filepath = django_file.file.name

        self.add_text_to_file(filepath, 'abc')

        self.assertEquals('abc', self.get_content_of_file(filepath))


class FileSystemDjangoTestCaseTearDownTest(FileSystemDjangoTestCase):

    def test_teardown_must_delete_all_created_files_in_tests(self):
        directory = self.create_temp_directory()
        filepath1 = self.create_temp_file()
        filepath2 = self.create_temp_file_with_name(directory, 'x.txt')

        self.fdf_teardown()

        self.assertFileDoesNotExists(filepath1)
        self.assertFileDoesNotExists(filepath2)

    def test_teardown_must_delete_files_with_content_too(self):
        filepath = self.create_temp_file()
        self.add_text_to_file(filepath, 'abc')

        self.fdf_teardown()

        self.assertFileDoesNotExists(filepath)

    def test_teardown_must_delete_all_created_directories_in_tests(self):
        directory = self.create_temp_directory()

        self.fdf_teardown()

        self.assertDirectoryDoesNotExists(directory)


class FileSystemDjangoTestCaseTearDownFrameworkConfigurationTest(FileSystemDjangoTestCase):

    def tearDown(self):
        super(FileSystemDjangoTestCaseTearDownFrameworkConfigurationTest, self).tearDown()

        self.assertFileDoesNotExists(self.filepath1)
        self.assertFileDoesNotExists(self.filepath2)
        self.assertDirectoryDoesNotExists(self.directory)

    def test_creating_directory_and_files_for_the_testcase(self):
        self.directory = self.create_temp_directory()
        self.filepath1 = self.create_temp_file()
        self.filepath2 = self.create_temp_file_with_name(self.directory, 'x.txt')
