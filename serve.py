from waitress import serve

from crm.wsgi import application

if __name__ == '__main__':
    serve(application, port='8004')