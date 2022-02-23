import logging

import jsonpickle
from django.db import transaction

from apps.async_requests.commands.command import Command
from apps.async_requests.models import CommandModel

logger = logging.getLogger(__name__)


class _Executor:
    _command_list = []

    def add_command(self, command: Command):
        # add command to database
        model = CommandModel(data=jsonpickle.encode(command))
        model.save()

    def remove_command(self, command: Command):
        self._command_list.remove(command)

    def __get_merged_commands(self) -> list:
        index_map = {}
        output = []
        # get commands from database
        objects = CommandModel.objects.all()
        self._command_list = [jsonpickle.decode(x.data) for x in objects]
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
                    command.timer = command.backoff_factor**command.times_delayed
                    failed_list.append(command)
        # remove all commands from database, and add back the failed ones
        with transaction.atomic():
            objects = [CommandModel(data=jsonpickle.encode(x)) for x in failed_list]
            CommandModel.objects.all().delete()
            CommandModel.objects.bulk_create(objects)
