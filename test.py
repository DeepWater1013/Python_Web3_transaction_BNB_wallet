# # using SendGrid's Python Library
# # https://github.com/sendgrid/sendgrid-python
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# import base64
# from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

# message = Mail(
#     from_email='robertyhamilton@gmail.com',
#     to_emails='grasshopper1013@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')

# with open('result.csv', 'rb') as f:
#     data = f.read()
#     f.close()
# encoded_file = base64.b64encode(data).decode()
# attachedFile = Attachment(
#     FileContent(encoded_file),
#     FileName('result.csv'),
#     FileType('application/csv'),
#     Disposition('attachment')
# )
# message.attachment = attachedFile

# try:
#     # ppp = os.environ.get('SENDGRID_API_KEY')
#     sg = SendGridAPIClient('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')
#     # print(ppp)
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)

from hexbytes import HexBytes

ppp = HexBytes('0x53b983fe73e16f6ed8178f6c0e0b91f23dc9dad4cb30d0831f178')


print(ppp)
ttt = ppp.hex()
qqq = str(ppp.hex())
print("0x053b983fe73e16f6ed8178f6c0e0b91f23dc9dad4cb30d0831f178" == qqq)
print(ttt, qqq)
print(ttt==qqq)
