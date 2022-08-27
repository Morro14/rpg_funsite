from .models import OneTimeCode


def code_delete(code_id):

    code = OneTimeCode.objects.get(pk=code_id)
    print(code)
    code.delete()
