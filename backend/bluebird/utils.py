import openpyxl
import requests
import json
import uuid
import os
from typing import List

from bluebird.models import (KLASS_TYPES, Contragent, ActUNGen, CountUNGen)
from bluebird.serializers import ContragentFullSerializer

from django.http import Http404
from django.template.loader import render_to_string

import pdfkit

from bluebird.dadata import (suggestions_response_from_dict,
                             Result_response_from_suggestion)


MIN_INNN_LEN = 10
MAX_INN_LEN = 12

TOKEN = os.environ.get('DADATA_TOKEN', '')
URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'


def parse_from_file(xlsx_file):
    xl = openpyxl.load_workbook(xlsx_file)
    sheet = xl.worksheets[0]
    results = []
    for row in sheet.iter_rows(min_row=3, max_row=42, min_col=2, max_col=5,
                               values_only=True):
        a, b, c, d = row
        # print('|', a, '|', b, '|', c, '|', d, '|')
        if a is not None:
            if MIN_INNN_LEN > len(str(a)) or len(str(a)) > MAX_INN_LEN:
                raise Exception(('200', 'Inn is wrong.'))
            else:
                if d != '' and 0 < d < len(KLASS_TYPES):
                    klass = KLASS_TYPES[d][0]
                else:
                    klass = 0
                tmp_obj = {
                    'inn': int(a),
                    'physical_address': b,
                    'excell_name': c,
                    'klass': klass
                }
                results.append(tmp_obj)
        else:
            continue
    return results


def get_object(pk, klass):
    try:
        return klass.objects.get(pk=pk)
    except klass.DoesNotExist:
        raise Http404


def get_dadata_data(contragent_inn: int) -> dict:
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": f"Token {TOKEN}"}
    data = {"query": contragent_inn}
    r = requests.post(
        URL,
        data=json.dumps(data),
        headers=headers,
        timeout=(3.0, 5.0),
    )
    return r.json()


def get_data(id: int):
    contragent = get_object(id, Contragent)
    data = get_dadata_data(contragent.inn)
    sug_d = suggestions_response_from_dict(data)
    if sug_d:
        if len(sug_d.suggestions):
            for d in sug_d.suggestions:
                is_result = d.data.state.status == 'ACTIVE'
                if is_result:
                    result = Result_response_from_suggestion(d)
                    serializer = ContragentFullSerializer(contragent,
                                                          data=result.data)
                    if serializer.is_valid():
                        serializer.save()
                        return {'inn': contragent.inn, 'status': "OK"}
            return {'inn': contragent.inn, 'status': "Not OK",
                    'errors': serializer.errors}
        else:
            return {'inn': contragent.inn,
                    'status': "0 length suggestion, something wrong."}
    else:
        return {'inn': contragent.inn,
                'status': "No suggestions. Check, DADATA is availiable?"}


def generate_documents(data: List, contragent: Contragent):

    for d in data:

        d['uniq_num_id'] = ActUNGen.create(d['curr_date'], contragent)
        generate_document(generate_act(d, contragent), 'act.pdf')

        d['uniq_num_id'] = CountUNGen.create(d['curr_date'], contragent)
        generate_document(generate_pay_count(d, contragent), 'count.pdf')


def generate_act(data: dict, contragent: Contragent):
    data['consumer'] = contragent
    return render_to_string('act.html', context=data)


def generate_pay_count(data: dict, contragent: Contragent):
    data['consumer'] = contragent
    return render_to_string('count.html', context=data)


def generate_count_fact(data: dict, contragent: Contragent):
    data['consumer'] = contragent
    return render_to_string('count_fact.html', context=data)


def generate_document(text: str, name: str, **kwargs):
    pdfkit.from_string(text, name, **kwargs)


def create_unique_id():
    return str(uuid.uuid4())
