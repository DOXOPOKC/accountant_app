import json
from dataclasses import dataclass, field
from typing import Optional, List, Any, Union, Dict
from datetime import date


@dataclass
class OPF:
    type_opf: Optional[str] = None
    code: Optional[str] = None
    full: Optional[str] = None
    short: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> Union['OPF', None]:
        if isinstance(obj, dict):
            type_opf = str(obj.get('type_opf', None))
            code = str(obj.get('code', None))
            full = str(obj.get('full', None))
            short = str(obj.get('short', None))
            return OPF(type_opf, code, full, short)
        return None


@dataclass
class NameModel:
    full_with_opf: Optional[str] = None
    short_with_opf: Optional[str] = None
    latin: Optional[str] = None
    full: Optional[str] = None
    short: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> Union['NameModel', None]:
        if isinstance(obj, dict):
            full_with_opf = str(obj.get('full_with_opf', None))
            short_with_opf = str(obj.get('short_with_opf', None))
            latin = str(obj.get('latin', None))
            full = str(obj.get('full', None))
            short = str(obj.get('short', None))
            return NameModel(full_with_opf, short_with_opf,
                             latin, full, short)
        return None


@dataclass
class AddressData:
    source: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> Union['AddressData', None]:
        if isinstance(obj, dict):
            source = obj.get('source', None)
            return AddressData(source)
        return None


@dataclass
class AddressModel:
    value: Optional[str] = None
    unrestricted_value: Optional[str] = None
    data: Optional[AddressData] = None

    @staticmethod
    def from_dict(obj: Any) -> Union['AddressModel', None]:
        if isinstance(obj, dict):
            value = obj.get('value', None)
            unrestricted_value = obj.get('unrestricted_value', None)
            data = AddressData.from_dict(obj.get('data', dict()))
            return AddressModel(value, unrestricted_value, data)
        return None


@dataclass
class State:
    status: Optional[str] = None
    actuality_date: None = None
    registration_date: None = None
    liquidation_date: None = None

    @staticmethod
    def from_dict(obj: Any) -> Union['State', None]:
        if isinstance(obj, dict):
            status = obj.get('status', None)
            actuality_date = obj.get('actuality_date', None)
            registration_date = obj.get('registration_date', None)
            liquidation_date = obj.get('liquidation_date', None)
            return State(status, actuality_date, registration_date,
                         liquidation_date)
        return None


@dataclass
class Management:
    name: Optional[str] = None
    post: Optional[str] = None
    disqualified: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> Union['Management', None]:
        if isinstance(obj, dict):
            name = obj.get('name', None)
            post = obj.get('post', None)
            disqualified = obj.get('disqualified', None)
            return Management(name, post, disqualified)
        return None


@dataclass
class Data:
    citizenship: Optional[str] = None
    source: Optional[str] = None
    qc: Optional[str] = None
    hid: Optional[str] = None
    type_enum: Optional[str] = None
    state: Optional[State] = None
    opf: Optional[OPF] = None
    name: Optional[NameModel] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None
    ogrn: Optional[str] = None
    okpo: Optional[str] = None
    okved: Optional[str] = None
    okveds: Optional[List] = None
    authorities: Optional[List] = None
    documents: Optional[List] = None
    licenses: Optional[List] = None
    finance: Optional[str] = None
    address: Optional[AddressModel] = None
    phones: Optional[List] = None
    emails: Optional[List] = None
    ogrn_date: None = None
    okved_type: Optional[str] = None
    employee_count: Optional[str] = None

    capital: Optional[str] = None
    management: Optional[Management] = None
    founders: Optional[List[str]] = None
    managers: Optional[List[str]] = None
    branch_type: Optional[str] = "MAIN"
    branch_count: Optional[int] = 0

    @staticmethod
    def from_dict(obj: Any) -> Union['Data', None]:
        if isinstance(obj, dict):
            citizenship = obj.get('citizenship', None)
            source = obj.get('source', None)
            qc = obj.get('qc', None)
            hid = obj.get('hid', None)
            type_enum = obj.get('type', None)
            state = State.from_dict(obj.get('state', None))
            opf = OPF.from_dict(obj.get('opf', None))
            name = NameModel.from_dict(obj.get('name', None))
            inn = obj.get('inn', None)
            kpp = obj.get('kpp', 0)
            ogrn = obj.get('ogrn', 0)
            okpo = obj.get('okpo', None)
            okved = obj.get('okved', None)
            okveds = obj.get('okveds', None)
            authorities = obj.get('authorities', None)
            documents = obj.get('documents', None)
            licenses = obj.get('licenses', None)
            finance = obj.get('finance', None)
            address = AddressModel.from_dict(obj.get('address', dict()))
            phones = obj.get('phones', None)
            emails = obj.get('emails', None)
            ogrn_date = obj.get('ogrn_date', None)
            okved_type = obj.get('okved_type', None)
            employee_count = obj.get('employee_count', None)

            capital = obj.get('capital', None)
            management = Management.from_dict(obj.get('management', dict()))
            founders = obj.get('founders', None)
            managers = obj.get('managers', None)
            branch_type = obj.get('branch_type', "MAIN")
            branch_count = obj.get('branch_count', 0)

            return Data(citizenship, source, qc, hid, type_enum, state,
                        opf, name, inn, kpp, ogrn, okpo, okved, okveds,
                        authorities, documents, licenses, finance, address,
                        phones, emails, ogrn_date, okved_type, employee_count,
                        capital, management, founders, managers, branch_type,
                        branch_count)
        return None


@dataclass
class Suggestion:
    value: Optional[str] = None
    unrestricted_value: Optional[str] = None
    data: Optional[Data] = None

    @staticmethod
    def from_dict(obj: Any) -> Union['Suggestion', None]:
        if isinstance(obj, dict):
            value = obj.get('value', None)
            unrestricted_value = obj.get('unrestricted_value', None)
            data = Data.from_dict(obj.get('data', None))
            return Suggestion(value, unrestricted_value, data)
        return None


@dataclass
class Suggestions_Response:
    suggestions: List[Optional[Suggestion]] = field(default_factory=list)

    @staticmethod
    def parse_from_dict(obj: Any) -> Union['Suggestions_Response', None]:
        if isinstance(obj, dict):
            is_suggestion = obj.get('suggestions', list())
            if is_suggestion:
                suggestions = [Suggestion.from_dict(d) for d in is_suggestion]
            return Suggestions_Response(suggestions)
        return None


def result_response_from_suggestion(response: Suggestion):
    data: Dict[str, Any] = dict()
    if isinstance(response.data, Data):

        name = response.data.name
        data['dadata_name'] = None
        if name:
            data['dadata_name'] = name.full_with_opf or None

        ogrn = response.data.ogrn
        data['ogrn'] = None
        if ogrn:
            data['ogrn'] = int(ogrn)

        kpp = response.data.kpp
        data['kpp'] = None
        if kpp:
            data['kpp'] = int(kpp)

        if response.data.management:
            data['director_status'] = response.data.management.post
            data['director_name'] = response.data.management.name
        data['creation_date'] = date.fromtimestamp(
            int(int(response.data.state.registration_date) / 1000))
        data['is_func'] = response.data.state.status == 'ACTIVE'
        data['okved'] = response.data.okved
        data['legal_address'] = response.data.address.data.source
    return data


def suggestions_response_from_dict(s: Any) -> Union['Suggestions_Response',
                                                    None]:
    return Suggestions_Response.parse_from_dict(s)


def parse_suggestions(json_string: str):
    return suggestions_response_from_dict(json.loads(json_string))
