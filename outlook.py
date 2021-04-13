import win32com
import win32com.client
import os


class Outlook:
    
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application")

    def send_mail(self, to, subject, body=None, html_body=None, attachments=None, bcc=None) -> None:        
        mail = self.outlook.CreateItem(0)
        mail.To = to
        mail.Subject = subject
        if bcc:
            mail.BCC = bcc
        if body:
            mail.Body = body
        if html_body:
            mail.HTMLBody = '<style>h5{font-style:italic;font-family:""Times New Roman""}</style>' + html_body + \
                            '<h5>Данное письмо сформировано автоматически программным роботом, отвечать на него ' \
                            'не нужно. При возникновении вопросов оформите, пожалуйста, обращение в поддержку по ' \
                            'направлению роботизации: письмом на 1111 или на портале самообслуживания».</h5>'
        if isinstance(attachments, str):
            mail.Attachments.Add(Source=attachments)
        elif isinstance(attachments, list):
            if attachments:
                for att in attachments:
                    mail.Attachments.Add(Source=att)
        else:
            raise Exception('Send e-mail exception: Во вложении должна быть ссылка на файл или список(str) с ссылками на файлы')
        mail.Send()
        # Удаляем файлы из каталога
        #for faile in attachments:
        #    os.remove(faile)            

    @staticmethod
    def save_attach(self, message, path) -> str:
        for att in message.Attachments:
            save_path = os.path.join(path, att.FileName)
            att.SaveAsFile(save_path)
            return save_path







