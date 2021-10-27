import jsonpickle
from django.test import TestCase

from apps.async_requests.factory import Factory
from apps.async_requests.models import CommandModel
from mocks.command import MockCommand, SecondMockCommand


class ExecutorTestCase(TestCase):
    def setUp(self) -> None:
        self.executor = Factory.get_executor()

    def tearDown(self) -> None:
        self.executor._command_list.clear()
        CommandModel.objects.all().delete()
        super().tearDown()

    def assert_command_list_size(self, size: int):
        self.assertEqual(size, len(CommandModel.objects.all()))

    def test_executor_add(self):
        # setup - none
        command = MockCommand(True, 1)

        # act
        self.executor.add_command(command)

        # test
        self.assert_command_list_size(1)

    # def test_executor_remove(self):
    #     # setup
    #     command = MockCommand(True, 1)
    #     self.executor.add_command(command)

    #     # act
    #     self.executor.remove_command(command)

    #     # test
    #     self.assert_command_list_size(0)

    def test_executor_two_mergeable_commands(self):
        # setup
        self.executor.add_command(MockCommand(True, 1))
        self.executor.add_command(MockCommand(True, 2))

        # act
        self.executor.execute()

        # test
        self.assert_command_list_size(1)
        self.assertEqual(jsonpickle.decode(CommandModel.objects.all()[0].data).parameters, [1, 2])

    def test_executor_two_unmergeable_commands(self):
        # setup
        self.executor.add_command(MockCommand(False, 1))
        self.executor.add_command(MockCommand(False, 2))

        # act
        self.executor.execute()

        # test
        self.assert_command_list_size(2)
        self.assertEqual(jsonpickle.decode(CommandModel.objects.all()[0].data).parameters, [1])
        self.assertEqual(jsonpickle.decode(CommandModel.objects.all()[1].data).parameters, [2])

    def test_executor_two_mergeable_one_unmergeable_commands(self):
        # setup
        self.executor.add_command(MockCommand(True, 1))
        self.executor.add_command(MockCommand(True, 2))
        self.executor.add_command(MockCommand(False, 3))

        # act
        self.executor.execute()

        # test
        self.assert_command_list_size(2)
        self.assertEqual(jsonpickle.decode(CommandModel.objects.all()[0].data).parameters, [1, 2])
        self.assertEqual(jsonpickle.decode(CommandModel.objects.all()[1].data).parameters, [3])

    def test_executor_two_sets_of_two_mergeable_commands(self):
        # setup
        self.executor.add_command(MockCommand(True, 1))
        self.executor.add_command(MockCommand(True, 2))
        self.executor.add_command(SecondMockCommand(True, 3))
        self.executor.add_command(SecondMockCommand(True, 4))

        # act
        self.executor.execute()

        # test
        self.assert_command_list_size(2)
        self.assertEqual(jsonpickle.decode(CommandModel.objects.all()[0].data).parameters, [1, 2])
        self.assertEqual(jsonpickle.decode(CommandModel.objects.all()[1].data).parameters, [3, 4])

    def test_executor_backoff(self):
        # setup
        self.executor.add_command(MockCommand(True, 1))

        # act
        self.executor.execute()

        # test
        test = jsonpickle.decode(CommandModel.objects.all()[0].data)
        self.assertEqual(test.timer, 2)
