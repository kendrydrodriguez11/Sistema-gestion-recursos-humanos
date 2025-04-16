from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pdfkit
import os
from django.template.loader import get_template

def get_image(image):
    if image:
        return '{}{}'.format(settings.MEDIA_URL, image)
    return '/static/images/empty.png'

def generate_pdf(template_name, context, filename):
    template = get_template(template_name)
    
    html = template.render(context)
    
    pdf_path = os.path.join(settings.MEDIA_ROOT, filename)

    pdf_folder = os.path.dirname(pdf_path)

    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    path_wkhtmltopdf = b"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdfkit.from_string(html, pdf_path, configuration=config)
    return pdf_path

def send_email(destinatario, asunto, cuerpo_mensaje, filename):
    mensaje = MIMEMultipart()
    mensaje['From'] = settings.EMAIL_HOST_USER
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    if filename is not None:
        with open(filename, 'rb') as f:
            adjunto = MIMEApplication(f.read(), _subtype='pdf')
            adjunto.add_header('Content-Disposition', 'attachment', filename=filename)
            mensaje.attach(adjunto)

    mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    server.sendmail(settings.EMAIL_HOST_USER, destinatario, mensaje.as_string())

    server.quit()
