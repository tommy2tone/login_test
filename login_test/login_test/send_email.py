from pyramid.session import JSONSerializer
from pyramid.session import SignedCookieSessionFactory
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from pyramid.url import route_url


def send_confirmation_email(email):
    mailer = Mailer(host='smtp.gmail.com',
                port=465,
                username='thomas.hildebrand11@gmail.com',
                password='@Testing1234',
                ssl=True)

    confirm_serializer = JSONSerializer()

    token = confirm_serializer.dumps(email)
    #link = route_url('register', token=token, _external=True)
    #print(token)
    
    subject = "Welcome to Handy Money.  Please verify your email."
    body = 'Please verify your email by clicking this link:  '
    
    message = Message(subject=subject,
            sender='thomas.hildebrand11@gmail.com',
            recipients=[email],
            body=body
                    )

    #mailer.send_immediately(message)

   