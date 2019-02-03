# STEP 1: import parser class
from pdf_parser import PDFParser

# STEP 2: instantiate class
parser = PDFParser()

# STEP 3: get available forms (i9, etc.)
forms = parser.available_forms()
print(forms)

# STEP 4: get form details (i.e. array of fields/questions object)
details = parser.form_details('dmv44')
print(details)

# STEP 5: fill form with form_name and answers dict, returns bytes
dummy_answers = {'ssn': '123456789', 'first_name': 'lil\'', 'last_name': 'pea', 'middle_name': '', 'address': '21 Pea Rd', 'apt_number': '1c', 'city': 'New York', 'state': 'NY', 'date_of_birth': '02022019', 'telephone_number': '917-PEA-PEA', 'applying_for': 1, 'purpose': 4, 'organ': 1}

filled_form = parser.fill_form('dmv44', dummy_answers)

# for debugging
from pdf_utils import save
save(filled_form, 'filled_test.pdf')
