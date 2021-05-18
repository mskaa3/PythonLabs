import pytest


httpMethod = ("PUT", "OPTIONS", "CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "TRACE")
code = ("HTTP/1.1", "HTTP/1.0", "HTTP/2.0")


class noneException(Exception):
    pass


class TypeError(Exception):
    pass


class BadRequestTypeError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


class ValueError(Exception):
    pass


class HTTP_request:
    def __init__(self, path):
        my_list = path.split(' ')
        if len(my_list) != 3:
            raise noneException
        else:
            if str(my_list[0]) in httpMethod:
                self.request = my_list[0]
            else:
                raise BadRequestTypeError
            if '/' == my_list[1][0]:
                self.path = my_list[1]
            else:
                raise ValueError
            if my_list[2] in code:
                self.protocol = my_list[2]
            else:
                raise BadHTTPVersion

    def __str__(self):
        return f'request type: {self.request},path {self.path}, http:{self.protocol}'


def reqstr2obj(request_string):
    if type(request_string) != str:
        raise TypeError
    try:
        return HTTP_request(request_string)
    except noneException:
        return None

# 4. It doesnt have to return anything, its just have to raise a proper exception, because
# test is about the exception itself


def test_reqstr2obj1():
    with pytest.raises(TypeError):
        reqstr2obj(3)


def test_reqstr2obj2():
    assert type(HTTP_request('GET / HTTP/1.1')) == HTTP_request


def test_reqstr2obj3():
    assert HTTP_request('GET / HTTP/1.1').request == 'GET' and \
           HTTP_request('GET / HTTP/1.1').path == '/' and\
           HTTP_request('GET / HTTP/1.1').protocol == 'HTTP/1.1'


def test_reqstr2obj4():
    line = 'CONNECT /blabla HTTP/1.1'
    new_list = line.split(' ')
    fun = reqstr2obj(line)
    assert fun.request == new_list[0] \
        and fun.path == new_list[1] \
        and fun.protocol == new_list[2]


def test_reqstr2obj5():
    assert reqstr2obj('GET  / HTTP/1.1"') is None


def test_reqstr2obj6():
    with pytest.raises(BadRequestTypeError):
        reqstr2obj("DOWNLOAD /movie.mp4 HTTP/1.1")


def test_reqstr2obj7():
    with pytest.raises(BadHTTPVersion):
        reqstr2obj("POST /movie.mp4 HTTP/54.1")


def test_reqstr2obj8():
    with pytest.raises(ValueError):
        reqstr2obj("GET movie.mp4 HTTP/1.1")


if __name__ == '__main__':
    print(HTTP_request('GET /new HTTP/1.1').__str__())
