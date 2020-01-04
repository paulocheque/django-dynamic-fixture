from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, StaticSequentialDataFixture
from django_dynamic_fixture.fixture_algorithms.random_fixture import RandomDataFixture


class FixtureFactory:
    @staticmethod
    def get(data_fixture):
        if data_fixture == 'static_sequential':
            return SequentialDataFixture()
        elif data_fixture == 'sequential':
            return SequentialDataFixture()
        elif data_fixture == 'random':
            return RandomDataFixture()
        return data_fixture