from .models import Journal


def get_or_create_journal(pack):
    journal = Journal.objects.get_or_create(pack=pack)
    return journal


def add_record_to_journal(pack, user):
    journal = get_or_create_journal(pack)
    return journal.add_record(user)
