from django.test import TestCase


# Testing wizard views: https://schinckel.net/2019/08/30/testing-wizardview-in-django/
class WizardViewTestCase(TestCase):
    @classmethod
    def wizard_has_validation_error(cls, response) -> bool:
        """
        Django returns 200 on a form validation error.
        Use `response.context_data["form"].is_bound` to check form validation error.
        If response is a re-rendering of the same form, it will be bound, otherwise it won't.

        :param response:
        :return: boolean indicating presence of validation error
        """
        return response.context_data["form"].is_bound

    def get_wizard_response(self, url: str, data: dict):
        """
        Simulates a successful wizard sequence. Asserts no validation errors in each step.

        :param url:
        :param data: dictionary of { "step_name": { "field": "value" } }
        :return: successful response
        """
        response = self.client.get(url)
        while response.status_code != 302:  # while still within the wizard
            self.assertEqual(200, response.status_code)
            self.assertFalse(self.wizard_has_validation_error(response))

            form = response.context_data["form"]
            view = response.context_data["view"]
            wizard = response.context_data["wizard"]
            wizard_name = wizard["management_form"].prefix

            current_step = view.storage.current_step

            if hasattr(form, "forms"):  # custom handling for formsets
                current_step_data = data.get(current_step, [])
                response = self.get_wizard_step_response_from_formsets(
                    wizard_name, form, current_step, current_step_data
                )
            else:
                current_step_data = data.get(current_step, {})  # get corresponding data, return {} if null
                response = self.get_wizard_step_response(url, wizard_name, current_step, current_step_data)
        return response

    def get_wizard_step_response(self, url: str, wizard: str, step: str, data: dict):
        """
        Simulates a wizard step.

        :param url:
        :param wizard: name of wizard (snake_case)
        :param step: name of wizard step (snake_case)
        :param data: dictionary of { "field": "value" }
        :return:
        """
        data = self.create_wizard_step_data(wizard, step, data)
        response = self.client.post(url, data)
        return response

    @classmethod
    def get_wizard_step_response_from_formsets(cls, wizard: str, form, step: str, data: dict):
        """
        Simulates a wizard step. Custom handling for formsets.
        :param wizard: name of wizard (snake_case)
        :param form:
        :param step: name of wizard step (snake_case)
        :param data: dictionary of { "field": "value" }
        :return: request data
        """
        step_data = data.get(step, [])
        output = {f"{step}-{key}": value for key, value in form.management_form.initial.items()}
        for i, _form in enumerate(form.forms):
            form_data = step_data[i] if len(step_data) > i else {}
            output.update(
                {
                    f"{form.prefix}-{field}": form_data.get(field, form.initial.get(field))
                    for field in form.fields
                    if field in form_data or field in form.initial
                }
            )

        # add wizard management form step data
        output[f"{wizard}-current_step"] = step
        return data

    @classmethod
    def create_wizard_step_data(cls, wizard: str, step: str, data: dict) -> dict:
        """
        Create form data for a wizard step.

        :param wizard:  name of wizard (snake_case)
        :param step: name of wizard step (snake_case)
        :param data: dictionary of { "field": "value" }
        :return: request data
        """
        output = {f"{step}-{field}": value for (field, value) in data.items()}

        # add wizard management form step data
        output[f"{wizard}-current_step"] = step
        return output

    @staticmethod
    def get_form(response):
        return response.context_data["form"]
