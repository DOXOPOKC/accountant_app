import os
from django import forms


def scan_templates_dir():
    scan = os.scandir(path='templates/')
    file_list = []
    dir_list = []
    for f in scan:
        if f.is_file():
            file_list.append(convert_to_choice(f.path))
        if f.is_dir():
            dir_list.append(f)
    while len(dir_list):
        scan = os.scandir(dir_list.pop(0))
        for f in scan:
            if f.is_file():
                file_list.append(convert_to_choice(f.path))
            if f.is_dir():
                dir_list.append(f)
    return sorted(file_list, key=lambda x: x[1])


def convert_to_choice(file_path):
    tmp_name_str = str(file_path)
    t_name = tmp_name_str[tmp_name_str.rfind('/')+1:tmp_name_str.rfind('.')]
    return (file_path, t_name)


class TemplateModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TemplateModelForm, self).__init__(*args, **kwargs)
        self.fields['template_path'].widget = forms.widgets.Select(
            choices=scan_templates_dir())
