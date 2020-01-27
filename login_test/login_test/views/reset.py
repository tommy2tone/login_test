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


@view_config(route_name='reset_email', renderer='../templates/reset_email.jinja2')
def reset_email(request): 
    session = request.session
    if 'form.submitted' in request.params:
        email = request.params['email_name']

        #   Create session to store email and use in reset_password view
        session['email'] = email
  
        # If statement to check if user exist in db.  If True, change email_confirmed column to 
        # 0 and redirect user to reset_email view
       
        if request.dbsession.query(models.User).filter(models.User.email == email).count() == 1:
            user = request.dbsession.query(models.User).filter(models.User.email == email).first()
            user.email_confirmed = 0
            request.dbsession.add(user)
            return HTTPFound(request.route_url('reset_password', message = email))
                    

        #Add else block to inform user email does not exist and to try again or create account
        else:
            next_url = request.route_url('register')
            msg = "The email entered does not exist.  Please try again or create an account."
            return {'message' : msg, 'link' : next_url, 'label' : 'Register'}
    
    return {}
    

@view_config(route_name='reset_password', renderer='../templates/reset_password.jinja2')
def reset_password(request):
    session = request.session
    
    if 'form.submitted' in request.params:
        new_password = request.params['password']
        new_reenter_password = request.params['reenter_password']

        #   Confirm passwords typed the same
        if new_password != new_reenter_password:
            return {'message' : 'Passwords do not match.  Try again.'}
            
        #   Helper functions to check password length, types of characters, and if the two form fields match
        if valid_password(new_password) != True:
            return {'message' : valid_password(new_password)}

        #   Update user's password
        user = request.dbsession.query(models.User).filter(models.User.email == session['email']).first()
        user.password_hash = user.set_password(new_password)
        update_user = models.User(password_hash = user.password_hash)
        
        #   Create unique token, link, and send confirmation email to user
        token = confirm_serializer.dumps(user.email, salt='email-confirmation') 
        link = request.route_url('confirm_email', token = token)  
        send_confirmation_email(user.email, link)

        #  Commit changes in db
        request.dbsession.add(update_user)

        #Redirect to view informing the user to check their email.  
        return HTTPFound(request.route_url('check_email'))
    return {}


