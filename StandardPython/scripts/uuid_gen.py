from email.mime import base
import uuid

def gen_random_uuid():
    base_uuid = uuid.uuid4()
    u = str(base_uuid)
    return u

def main():
    u = gen_random_uuid()
    print(u)

if __name__=="__main__":
    main()