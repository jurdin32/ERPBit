import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(subject, message, from_email, to_email=[], attachment=[]):
    """
    :param subject: Asunto del Email
    :param message: Cuerpo del mensaje, puede estar en HTML/CSS o en texto plano
    :param from_email: Email que realiza el envio
    :param to_email: Lista de emails al q se enviaran los mensajes: ["a@a.com", "b@b.com"]
    :param attachment: Lista de archivos que se adjuntaran al mensaje: ["file1.txt", "file2.txt"]
    """
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ", ".join(to_email)
        msg.attach(MIMEText(message, 'html'))
        for f in attachment:
            with open(f, 'rb') as a_file:
                basename = os.path.basename(f)
                part = MIMEApplication(a_file.read(), Name=basename)
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename
            msg.attach(part)
            print("Agregando archivo",str(f))
        email = smtplib.SMTP('smtp.webfaction.com',587)
        email.login('bitventas','johnny1987')
        email.sendmail(from_email, to_email, msg.as_string())
        print("mensaje:","El correo se envio..!!")
    except Exception as error:
        print("error:",error)

# send_email("Prueba de email","Aqui el mensaje a enviar","info@dizof.com",["j-h-diog@live.com.ar"],['D:\Drive\Proyectos_Drive\ERPBit\celeryapp.bat'])