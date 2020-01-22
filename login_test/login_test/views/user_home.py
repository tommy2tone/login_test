from pyramid.view import forbidden_view_config, view_config


@view_config(route_name='user_home', renderer='../templates/user_home.jinja2')
def register(request):
    return {}