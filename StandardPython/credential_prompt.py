import socket
import win32cred


def cred_prompt():
    host = socket.gethostname()
    data = win32cred.CredUIPromptForCredentials(host, 0, None, None, False, 0, None)
    account_name = data[0]
    password = data[1]
    result = f"Account Name: {account_name} Password: {password}"
    return result


def main():
    creds = cred_prompt()
    print(creds)

if __name__=="__main__":
    main()
