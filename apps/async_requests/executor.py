import logging

from apps.async_requests.commands.command import Command

logger = logging.getLogger(__name__)


class _Executor:

    _command_list = []
    _instance = None

    def add_command(self, command: Command):
        self._command_list.append(command)

    def remove_command(self, command):
        self._command_list.remove(command)

    def execute(self):
        temp_list = []
        failed_list = []

        for command in self._command_list:
            if command.timer == 0:
                self._command_list.remove(command)
                if command.can_merge():
                    for command2 in self._command_list:
                        if command2.can_merge() & type(command) == type(command2):
                            temp_list.append(command2)
                            self._command_list.remove(command2)

                    command.merge(temp_list)
            else:
                command.timer -= 1

            try:
                command.execute()
            except Exception as e:
                logger.error(repr(e))
                if (command.times_delayed == 3):
                    logger.error(repr(e))
                else:
                    logger.warning(repr(e))
                    command.times_delayed += 1
                    command.timer = command.backoff_factor ** command.times_delayed
                    failed_list.append(command)
                    failed_list.extend(temp_list)

            temp_list = []

        self._command_list.extend(failed_list)


def get_executor():
    if _Executor._instance is None:
        _Executor._instance = _Executor()
    return _Executor._instance
