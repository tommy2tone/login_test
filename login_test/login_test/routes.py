
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('confirm_email', '/confirm_email/{token}')
    config.add_route('check_email', '/check_email')
    config.add_route('user_home', '/user_home')
    config.add_route('reset_email', '/reset_email')
    config.add_route('reset_password', '/reset_password/')
   

