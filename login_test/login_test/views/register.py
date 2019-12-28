import bcrypt
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from .. import models
from .. send_email import send_confirmation_email


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    
    if 'form.submitted' in request.params:
        new_email = request.params['email_name']
        new_password = request.params['password']
        
        print(new_email + ' ' + str(new_password))
        
        # If statement to check if user exist in db.  If not, create new User object and 
        # send confirmation email to user with unique token.
        if request.dbsession.query(models.User).filter(models.User.email == new_email).count() == 0:
            user = User()
            user.name = new_email
            #user.password_hash = user.set_password(new_password)
            print(user.name)
            
            
        #send_confirmation_email(user.name)

    return {}