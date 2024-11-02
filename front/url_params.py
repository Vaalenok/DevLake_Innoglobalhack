import urllib.parse

def get_param(route, param_name):
    query_string = route.split('?', 1)[-1]  # Получаем строку запроса, если она есть
    params = urllib.parse.parse_qs(query_string)  # Парсим строку запроса в словарь
    return params.get(param_name, [None])[0]  # Извлекаем значение параметра "param", если он существует