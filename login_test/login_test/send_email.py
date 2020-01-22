from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from email_config import host, port, username, password

def send_confirmation_email(email, link):
        email = email
        link = link

        mailer = Mailer(host=host,
                        port=port,
                        username=username,
                        password=password,
                        ssl=True)
    
    
        subject = "Welcome.  Please verify your email."
        body = f'Please verify your email by clicking this link: {link} ' 
        #Create html.jinja2 template for email body
        
        message = Message(subject=subject,
                sender=username,
                recipients=[email],
                body=body
                        )

        mailer.send_immediately(message)

   