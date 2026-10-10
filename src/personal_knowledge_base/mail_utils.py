import imaplib, ssl, email, os
from pathlib import Path
from imap_tools import MailBox
from pydantic import SecretStr
from dotenv import load_dotenv

#----------------------------------------------------------------------------------------
# establish a connection with the mail-serever, and return a handle to the email-folder
def connect_to_mail_folder(username: str, email_folder:str):
    print("connect_to_mail_folder()")
    # EMAIL_FOLDER = email_folder
    if (email_folder == ""):
        print("Error:  empty email folder!")
        return None

    MAIL_PASSWD = SecretStr(os.getenv("MAIL_SERVER_PASSWD", ""))
    if not MAIL_PASSWD.get_secret_value():
        raise RuntimeError("MAIL_SERVER_PASSWD is not set")

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    imap_ssl_host = 'imap.mail.yahoo.com' 
    imap_ssl_port = 993
    mail = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port, ssl_context=context)

    # Login to mail
    print("bfr login")
    # t = mail.login(username, MAIL_PASSWD.get_secret_value())
    try:
        mail.login(username, MAIL_PASSWD.get_secret_value())
        print ("Logged in uusername")
    except: 
        # imaplib.
        print ("Log in failed.")
        return None

    # print("aftr login")
    # rv, data = mail.search(None, email_folder)
    # if rv != 'OK':
    #     print ("Folder not found!")
    #     return None

    l = mail.list(directory='', pattern=email_folder)
    print ("len l = " + str(len(l)) )

    for i in l:
        print(str(i) + "   stam...")

    lc1 = l[1][0]
    print(lc1)
    if (lc1 == None):
        print("bfr returning 1st None")
        return None

    # text_data = lc1.decode('utf-8')
    # found_no_select = text_data.find("Noselect")

    # print("aftr lc11,  found_no_select = " + found_no_select)
    # print("type lc1 = " + type(lc1))
    # found_folder = lc1.find(email_folder)
    # print("found_folder = " + found_folder)
    
    # for i in mail.list(directory='', pattern=email_folder):
    #     print(str(i) + "   stam..")

    # if (l not in mail.list()[1]):
    #     print("bfr returning None")
    #     return None

    # print("bfr mail.select()")
    # mail.select(email_folder)

    # l = mail.list(directory='', pattern=email_folder)
    # print ("len l = " + str(len(l)) )
    
    # for i in l:
    #     print(i)

    # if (l[0] == None):
    #     return None

    print("bfr mail.select(),  email_folder = " + email_folder)
    mail.select(email_folder)
    return mail
    
    # try:
    #     if (mail.select(email_folder) == None):
    #         print("connect_to_mail_folder():   returning None")
    #         return None
    #     else:
    #         return mail
    # finally:
    #     print("except in select..")


#----------------------------------------------------------------------------------------
# save all the attachments from a specific email-folder of a user
def save_attachments(username: str, 
                     email_folder:str, 
                     save_folder: str) -> bool:

    # establish serever-connection
    folder_handle = connect_to_mail_folder(username, email_folder)
    if not folder_handle:
        print("save_attachments():  returning False")
        return False
    print("save_attachments():  after the check..")
    
    type, data = folder_handle.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()

    # loop over all the mails in the folder
    for id in id_list:
        print("id:" + str(id))
        typ, data = folder_handle.fetch(id, '(RFC822)')

        # convert byte literal to string
        raw_email = data[0][1]  
        try:
            raw_email_string = raw_email.decode('utf-8')
        except UnicodeDecodeError:
            print("bad raw_email decode!")
            continue
            
        email_message = email.message_from_string(raw_email_string)

        # download attachments
        attachment_types = ["docx", "doc", "xlsx", "xls", "pdf", "txt"]
        symbols = ['/', '=', '?', '%', '&', '$', '#', '*', '+', '-']
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            # make sure the file is from a type that we ant to save. if not - move to the next file
            file_name = part.get_filename()
            print(file_name)
            if (file_name):
                ftype = file_name.split(".")[-1]
            else:
                continue

            if not ftype in attachment_types:
                continue

            # make sure the file-name is valid 
            file_name = make_valid_filename(file_name)
            if (file_name == None):
                continue

            # save the file in a sub-folder(the name of the sender)
            if bool(file_name):
                sender = email_message['From']
                sender = sender.replace('<', '').replace('>', '')  
                sender = sender.split(" ")[0].replace('\"', '')
                if (sender[0] in symbols):
                    continue
                
                tpath = save_folder + '/' + str(sender)
                Path(tpath).mkdir(parents=True, exist_ok=True)
                file_path = tpath.__str__() + '/' + file_name

                print("attachment_path: " + file_path)
                print("save path: " + file_path + "\n")
                
                if not os.path.isfile(file_path):
                    print(file_name)
                    try:
                        fp = open(file_path, "wb")
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    except ValueError:
                        print("Bad value!")
                        return False
    return True

def save_texts(username: str,
               email_folder: str,
               save_folder: str):

    load_dotenv()
    MAIL_PASSWD = SecretStr(os.getenv("MAIL_SERVER_PASSWD", ""))
    if not MAIL_PASSWD.get_secret_value():
        raise RuntimeError("MAIL_SERVER_PASSWD is not set")
    
    mail_password = MAIL_PASSWD.get_secret_value()
    with MailBox('imap.mail.yahoo.com').login(username, mail_password, initial_folder=email_folder) as mb:
        for msg in mb.fetch(limit=25, reverse=True):
            sender = msg.from_
            sender = sender.replace('<', '').replace('>', '')  
            sender = sender.split(" ")[0].replace('\"', '')
            sender = sender.replace('@', '_')
            tpath = save_folder + '/' + str(sender)
            Path(tpath).mkdir(parents=True, exist_ok=True)
            subject_split = msg.subject.split()
            file_name = msg.subject
            if (len(subject_split) > 9):
                file_name = subject_split[0] + "_" + subject_split[1] + "_" + subject_split[2] + "_" + subject_split[3] +  "_" + subject_split[4] + "_" + subject_split[5] + "_" + subject_split[6] + subject_split[7] + "_" + subject_split[8]
            file_name = make_valid_filename(file_name) + ".txt" 
            file_path = tpath.__str__() + '/' + file_name
            print("file_path = " + file_path)
            fp = open(file_path, "wb")
            fp.write(msg.from_.encode())
            fp.write(msg.subject.encode())
            fp.write(msg.text.encode())
            fp.close()

            print(file_path)

#----------------------------------------------------------------------------------------
# Make sure that the file-name is valid by replacing non-valid characters
def make_valid_filename(file_name:str) -> str:
    file_name = file_name.replace(' ', '_')
    file_name = file_name.replace(',', '_')
    file_name = file_name.replace('?', '_')
    file_name = file_name.replace('=', '_')
    file_name = file_name.replace('\'', '_')
    file_name = file_name.replace('\\', '_')
    file_name = file_name.replace("\r", '_')
    file_name = file_name.replace("\n", '_')
    file_name = file_name.replace(':', '_')
    symbols = ['/', '=', '?', '%', '&', '$', '#', '*', '+', '-']

    return file_name if not file_name[0] in symbols else None