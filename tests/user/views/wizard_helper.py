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

    def get_wizard_response(self, url: str, step_data: dict):
        """
        Simulates a successful wizard sequence. Asserts no validation errors in each step.

        :param url:
        :param step_data:
        :return: successful response
        """
        response = self.client.get(url)
        while response.status_code != 302:  # while still within the wizard
            self.assertEqual(200, response.status_code)
            self.assertFalse(self.wizard_has_validation_error(response))

            form = response.context_data["form"]
            wizard = response.context_data["wizard"]
            view = response.context_data["view"]

            current_step = view.storage.current_step

            # If we have a formset, then we need to do custom handling
            if hasattr(form, "forms"):
                current_step_data = step_data.get(current_step, [])
                data = {f"{current_step}-{key}": value for key, value in form.management_form.initial.items()}
                for i, _form in enumerate(form.forms):
                    current_form_data = current_step_data[i] if len(current_step_data) > i else {}
                    data.update(
                        {
                            f"{_form.prefix}-{field}": current_form_data.get(field, _form.initial.get(field))
                            for field in _form.fields
                            if field in current_form_data or field in _form.initial
                        }
                    )
            else:
                # assume no formset
                current_step_data = step_data.get(current_step, {})  # get corresponding data, return {} if null
                data = {
                    f"{form.prefix}-{field}": current_step_data.get(field, form.initial.get(field))
                    for field in form.fields
                    if field in current_step_data or field in form.initial
                }
            # add wizard management form step data
            data[f"{wizard['management_form'].prefix}-current_step"] = current_step
            response = self.client.post(url, data)
        return response
