
import sendEmail as sendEmail

# This will send me an email each time it is run, please don't spam me

print ('Running')

body = 'This is a test email from python'
recipient = 'ryanpybus8596@gmail.com';
sendEmail.send_email(body,recipient);

print('Finished')
