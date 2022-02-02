from patreon import pstore
import patreon
import requests

global_services = [
    'signup'
]

per_id_services = []


def get_id_key(service, id):
    return 'captcha_{}_{}'.format(service, id)


def get_service_key(service):
    return 'captcha_{}'.format(service)


def get_ids_for_service(service):
    try:
        return pstore.get(get_service_key(service)) or []
    except Exception as e:
        return []


def set_ids_for_service(service, ids):
    pstore.set(get_service_key(service), ids)


def is_enabled(service, id=None):
    if id:
        return bool(pstore.get(get_id_key(service, id))) == True

    return bool(pstore.get(get_service_key(service))) == True


def disable_captcha_for_service(service, id=None):
    if id:
        disable_captcha_for_service_and_id(service, id)
        return

    pstore.set(get_service_key(service), False)


def disable_captcha_for_service_and_id(service, id):
    pstore.set(get_id_key(service, id), False)
    result = get_ids_for_service(service)
    result = list(set(result))
    result.remove(id)
    set_ids_for_service(service, result)


def enable_captcha_for_service_and_id(service, id):
    pstore.set(get_id_key(service, id), True)
    result = get_ids_for_service(service)
    result.append(id)
    result = list(set(result))
    set_ids_for_service(service, result)
    return


def enable_captcha_for_service(service, id=None):
    if id:
        enable_captcha_for_service_and_id(service, id)
        return

    pstore.set(get_service_key(service), True)


def check_response_against_recaptcha(recaptcha_response, request_ip):
    url = "https://www.google.com/recaptcha/api/siteverify"
    response = requests.post(url, data={
        'secret': patreon.config.recaptcha_key,
        'response': recaptcha_response,
        'remoteip': request_ip
    }).json()
    return response['success']


def captcha_response_is_valid(recaptcha_response, request_ip):
    if not recaptcha_response:
        return False
    return bool(check_response_against_recaptcha(recaptcha_response, request_ip))


def get_service_ids():
    return_dict = {}
    for service in global_services:
        result = get_ids_for_service(service)
        if result:
            return_dict[service] = result
    return return_dict
