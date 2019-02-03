

def parse_answers(answers, fields):
    pointer_values = {}
    for field_id in answers:
        answer_value = answers[field_id]
        field = fields[field_id]
        field_type = field['type']
        field_pointers = field['pointers']
        if field_type == 'char':
            if len(answer_value) != len(field_pointers):
                print("Warning: field %s expected %d chars but got %d" % (field_id, len(answer_value), len(field_pointers)))
                print("%s vs. %s" % (answer_value, field_pointers))
            for i, pointer in enumerate(field_pointers):
                val_char = answer_value[i]
                pointer_values[pointer] = val_char
        else:
            if field_type == 'option':
                field_options = field['options']
                answer_value_int = int(answer_value)

                field_pointer = field_pointers[answer_value_int]
                field_value = 'X'
            else:
                field_pointer = field_pointers[0]
                if field_type == 'bool':
                    if answer_value == 'yes':
                        field_value = 'X'
                    else:
                        field_value = ''
                else:
                    field_value = answer_value

            pointer_values[field_pointer] = field_value

    return pointer_values
