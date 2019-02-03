import pdf_utils
import model_utils
import answer_utils

class PDFParser():

    def __init__(self):
        self.forms = model_utils.available_models()
        self.models = {form_name: model_utils.load_form_model(form_name) for form_name in self.forms}

    # input: none
    # output: list of available form names
    def available_forms(self):
        return self.forms

    # input: form name
    # output: list of fields to fill in form [{'id': (field_id), 'question': (field question), 'type': ('text'/'bool')}]
    def form_details(self, form_name):
        if not self.check_form_exists(form_name):
            return

        fields = self.models[form_name]
        details = []
        for field in sorted(fields.values(), key=lambda x: x['idx']):
            details.append({'id': field['id'], 'question': field['name'], 'type': field['type'] if field['type'] != 'char' else 'text'})

        return details

    # input: form name and list of answers to fields in form {(field_id): (answer_value)}']
    # output: pdf form bytes
    def fill_form(self, form_name, answers):
        if not self.check_form_exists(form_name):
            return

        pointer_values = answer_utils.parse_answers(answers, self.models[form_name])
        print(pointer_values)
        filled_form = pdf_utils.fill_pdf(form_name, pointer_values)

        return filled_form

    def check_form_exists(self, form_name):
        if form_name not in self.forms:
            print('Requested form \'%s\' not in available forms. Try one of: %s' % (form_name, str(self.forms)))
            return False

        return True
        




