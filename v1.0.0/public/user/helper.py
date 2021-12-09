from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from requests import post

class helper():

    def check_user_exist(self, email):
        if User.objects.filter(email=email).exists():
            return True
        else:
            return False


def tcValidate(tc, first_name, last_name, birthday_year):
    """
        This function will validate the tc number
        :param tc: tc number
        :param first_name: first name
        :param last_name: last name
        :param birthday_year: birthday year
        :return: True if tc is valid, False if not
    """
    
    from re import search
    url = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"

    regex = r"(?:\<TCKimlikNoDogrulaResult\>)(true|false)(?:\<\/TCKimlikNoDogrulaResult\>)"

    headers = {'content-type': 'application/soap+xml'}
    
    body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
        <TCKimlikNo>{tc}</TCKimlikNo>
        <Ad>{first_name.encode().decode('utf-8').upper().replace('I', 'İ')}</Ad>
        <Soyad>{last_name.encode().decode('utf-8').upper().replace('I', 'İ')}</Soyad>
        <DogumYili>{birthday_year}</DogumYili>
        </TCKimlikNoDogrula>
    </soap12:Body>
    </soap12:Envelope>"""

    response = post(url, data=body.encode('utf-8'), headers=headers)
    result = search(regex, response.text)
    if result:
        return True if result.group(1) == 'true' else False
    else:
        return False


def check_user(user):
    return not user.is_authenticated


user_logout_required = user_passes_test(check_user, '/', None)


def auth_user_should_not_access(viewfunc):
    return user_logout_required(viewfunc)


# def check_user_tc(user):
#     return user.is_authenticated and not user.profile.is_tc_verified

# user_tc_required = user_passes_test(check_user_tc, '/', None)

# def tc_user_should_not_access(viewfunc):
#     return user_tc_required(viewfunc)


def tc_user_should_not_access(function):
    def is_tc_verified(u):
        return not u.profile.is_tc_verified

    actual_decorator = user_passes_test(is_tc_verified, '/', None)

    if function:
        return actual_decorator(function)
    else:
        return actual_decorator
