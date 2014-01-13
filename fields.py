from os import remove
from re import match
from subprocess import check_output
from fdfgen import forge_fdf

def get_fields(pdf_file):
    '''Uses pdftk to get a pdf's fields as a string, parses the string
    and returns the fields as a list of lists, where the field name is
    the first element in the list and its current value is the second
    element'''
    fields = []
    call = ['pdftk', pdf_file, 'dump_data_fields']
    try:
        data_string = check_output(call).decode('utf8')
    except FileNotFoundError:
        raise PdftkNotInstalledError('Could not locate PDFtk installation')
    data_list = data_string.split('\r\n')
    for index, line in enumerate(data_list):
        if line == '---':
            if index != 0:
                fields.append(field)
            field = ['', '']
        elif line:
            re_object = match(r'(\w+): (.+)', line)
            if re_object.group(1) == 'FieldName':
                field[0] = re_object.group(2)
            elif re_object.group(1) == 'FieldValue':
                field[1] = re_object.group(2)
    return fields

def write_pdf(source, fields, output):
    '''Takes source file path, list of fdf fields, and output path, and
    creates a filled-out pdf'''
    fdf = forge_fdf(fdf_data_strings=fields)
    fdf_file = open('data.fdf', 'wb')
    fdf_file.write(fdf)
    fdf_file.close()
    call(r'pdftk {0} fill_form data.fdf output {1}'.format(source, output))
    remove(r'data.fdf')
    
class PdftkNotInstalledError(Exception):
    pass