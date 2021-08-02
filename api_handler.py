from app.Common.api_constant import APIEndpoints
from app.factory.factory import Factory
import importlib


def lambda_handler(event, context):
    http_verb = event.get('context', dict()).get('http-method', None)
    api_name = event.get('context', dict()).get('resource-path', None)

    api_requested = "{api}/{verb}".format(api=api_name, verb=http_verb)
    print("API called : {api_requested}".format(api_requested=api_requested))

    api_module = APIEndpoints.api_endpoints.get(api_requested)

    if not api_module:
        print("Invalid API called")
        raise Exception("Invalid API called")

    try:
        function = "{function}".format(function=api_module['Function'])
        import_path = "app.Endpoint.{file}".format(file=api_module['File'])

        mode_import = importlib.import_module(name=import_path, package=function)
        func = getattr(mode_import, function)
        result = func(event, Factory())
        return result
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    event = {
        "body-json": {
            "user_name": "rahulbhave",
            "password": "123456789@"
        },
        'context': {
            'http-method': "POST",
            'resource-path': "login"

        }
    }
    lambda_handler(event, None)
