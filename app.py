from flask import Flask, request, Response
from hook import Hook

from dispatch import dispatch
import sys
import importlib as imp
import os

file_names = os.listdir(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins', '')
)
module_names = [
    f"plugins.{file_name[:-3]}"
    for file_name in file_names
    if os.path.isfile(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'plugins', '', file_name
        )
    )
]
modules = [imp.import_module(module_name) for module_name in module_names]
list_of_plugins = [module for module in modules if hasattr(module, 'EVENT')]

plugins = {}
for plugin in list_of_plugins:
    plugins[plugin.EVENT] = plugin

def new_request(request):

    new_hook = Hook()

    for arg in request.args:
        if arg[0] in new_hook.params:
            new_hook.params[arg[0]] = arg[1]

    return new_hook

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():

    hook = new_request(request)

    hook.checkwebhook()

    try:
        plugin = plugins[request.headers.get('X-Gitlab-Event')]
        data = plugin.run(request, hook.color, hook.hideAuthor, hook.hideBranch)
        if data == "empty":
            return Response(status=204)
        else:
            status = dispatch(data, hook.webhook)
            return Response(status=status)
    except KeyError:
        return Response(
            status=405, response="That event isn't supported by Githook (yet)."
        )
    except Exception:
        return Response(status=401)

def start_app(port='5000'):
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Check if a system argument of port was provided
    if '--port' in sys.argv:
        try:
            # Try and run with port argument
            start_app(sys.argv[2])
        except: 
            # Run on default port
            start_app()
    elif 'PORT' in os.environ:
        try:
            # Try and run with ENV port
            start_app(os.environ['PORT'])
        except:
            # Run on default port
            start_app()
    else: 
        # Run on default port
        start_app()