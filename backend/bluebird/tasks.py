from django.http import Http404

from django_q.tasks import async_task, Task

from blackbird.views import calculate


def calc_create_gen_async(contragent, pack, recreate: bool = False):
    try:
        async_task(calculate, contragent.contract_accept_date,
                   contragent.current_date, contragent.stat_value,
                   contragent.norm_value, pack, recreate,
                   hook=gen_async, group=pack.name_uuid)
    except AttributeError:
        raise Http404


def gen_async(task):
    from .utils import generate_documents
    if task.success:
        async_task(generate_documents, task.result, task.args[4], task.args[5],
                   hook=del_after_exec, group=task.group)
    else:
        del_after_exec(task)
        raise Http404


def del_after_exec(task):
    Task.delete_group(task.group)
