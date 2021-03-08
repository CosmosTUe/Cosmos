from django.test import TestCase

from apps.async_requests.factory import Factory
from mocks.command import MockCommand


class ExecutorTestCase(TestCase):
    def setUp(self) -> None:
        self.executor = Factory.get_executor()
        self.test_command = MockCommand(True, 1)
        self.executor.add_command(self.test_command)

    def tearDown(self) -> None:
        self.executor._command_list.clear()
        super().tearDown()

    def test_executor_add(self):
        self.executor.add_command(MockCommand(True, 2))
        self.assertTrue(len(self.executor._command_list) == 2)

    def test_executor_remove(self):
        self.executor.remove_command(self.test_command)
        self.assertTrue(len(self.executor._command_list) == 0)

    def test_executor_merge(self):
        self.executor.add_command(MockCommand(True, 2))
        self.executor.execute()
        self.assertTrue(len(self.executor._command_list) == 1)
        self.assertTrue(self.executor._command_list[0].parameters == [1, 2])

    def test_executor_backoff(self):
        self.executor.execute()
        self.assertTrue(self.executor._command_list[0].timer == 2)
