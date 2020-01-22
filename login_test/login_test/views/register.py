from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.security import remember, forget
from pyramid.view import forbidden_view_config, view_config
from .. import models
from .. send_email import send_confirmation_email
from .. valid_password import valid_password
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import secret


confirm_serializer = URLSafeTimedSerializer(secret.secret)


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request): 
    if 'form.submitted' in request.params:
        new_email = request.params['email_name']
        new_password = request.params['password']
        new_reenter_password = request.params['reenter_password']
    

        if new_password != new_reenter_password:
            return {'message' : 'Passwords do not match.  Try again.'}
        
        #   Helper functions to check password length, types of characters, and if the two form fields match
        if valid_password(new_password) != True:
            return {'message' : valid_password(new_password)}
  
        # If statement to check if user exist in db.  If not, create new User object and 
        # send confirmation email to user with unique token.
        if request.dbsession.query(models.User).filter(models.User.email == new_email).count() == 0:
            user = models.User()
            user.name = new_email
            user.password_hash = user.set_password(new_password) 
            new_user = models.User(email = user.name, password_hash = user.password_hash)
            token = confirm_serializer.dumps(user.name, salt='email-confirmation') 
            link = request.route_url('confirm_email', token = token)  
            send_confirmation_email(user.name, link)

            #Add new user to db
            request.dbsession.add(new_user)

            #Redirect to view informing the user to check their email.  Create template.
            return HTTPFound(request.route_url('check_email'))

            
                                        
        #Add else block to inform user email exist
        else:
            return {'message' : 'The email entered already exist.  Please try again.'}
    
    return {}
    

@view_config(route_name='confirm_email', renderer='../templates/confirm_email.jinja2') #Need template for confirm_email page
def confirm_email(request):
    token = request.matchdict['token']
    try:
        email = confirm_serializer.loads(token, salt='email-confirmation', max_age=432000)
        #Add if statement to change 'email_confirmed' column to True
        if email:
            user = request.dbsession.query(models.User).filter(models.User.email == email).first()
            user.email_confirmed = 1
            request.dbsession.add(user)
            return {'message' : f'Your email {email} has been confirmed!'}
    except SignatureExpired:
        return {'message' : 'The token has expired.  Please re-register.'}

@view_config(route_name='check_email', renderer='../templates/check_email.jinja2')
def check_email(request):
    return{}


@view_config(route_name='reset', renderer='../templates/reset.jinja2')
def reset(request):
    return {}