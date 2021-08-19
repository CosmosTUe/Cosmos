import logging

from apps.async_requests.commands.command import Command

logger = logging.getLogger(__name__)


class _Executor:
    _command_list = []

    def add_command(self, command: Command):
        # do the merging here!
        self._command_list.append(command)

    def remove_command(self, command: Command):
        self._command_list.remove(command)

    def __get_merged_commands(self) -> list:
        index_map = {}
        output = []
        for command in self._command_list:
            if not command.get_can_merge():
                output.append(command)
                continue

            # can_merge
            command_type = type(command).__name__
            if command_type not in index_map:
                output_index = len(output)
                output.append(command)
                index_map[command_type] = output_index
            else:
                output[index_map[command_type]].merge([command])

        self._command_list = output.copy()
        return output

    def execute(self):
        failed_list = []
        for command in self.__get_merged_commands():
            self._command_list.remove(command)
            try:
                command.execute()
            except Exception as e:
                if command.times_delayed == 3:
                    logger.error(repr(e))
                else:
                    logger.warning(repr(e))
                    command.times_delayed += 1
                    command.timer = command.backoff_factor ** command.times_delayed
                    failed_list.append(command)
        self._command_list.extend(failed_list)
