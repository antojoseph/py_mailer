#! /usr/bin/python
import cgi, os
import cgitb; cgitb.enable()
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def read_template(filename):
	with open(filename) as template:
		return template.read()

def blast(from_email,to_email,subject):

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = from_email
	msg['To'] = to_email
	text = "Please allow the Html Version\n"
	html =read_template("mail_template.html")

	# Login credentials
	username = 'user username here'
	password = "your password here"

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	msg.attach(part1)
	msg.attach(part2)

	# Open a connection to the SendGrid mail server
	s = smtplib.SMTP('smtp.sendgrid.net', 587)

	# Authenticate
	s.login(username, password)

	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.

	s.sendmail(from_email, to_email, msg.as_string())



	s.quit()



#cgi part starts here !

form = cgi.FieldStorage() 

# Get data from fields
mail_from = form.getvalue('mail_from')
mail_sub  = form.getvalue('mail_sub')
burst = form.getvalue('mail_count')
fileobject = form['file']
fname = fileobject.filename


#function to remove the temp uploaded file !
def del_file():
	os.system("rm /tmp/"+fname)


# Function to get file and save in the temp folder !
def read_file():

	content =fileobject.file.read()
	with open('/tmp/'+fname, 'w') as f:
		f.write(content)
		f.close()

read_file()


#opening the stored file and sending the mails .

with open('/tmp/'+fname) as csvfile:
    	spamreader = csv.reader(csvfile, delimiter=",", quotechar='|')

        for line in spamreader:
         	blast(mail_from,line[1],mail_sub)










