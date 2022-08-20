import clr
clr.AddReference("System")
clr.AddReference("System.Security")
import System.Text as Text
import System.Array as Array
import System.Byte as Byte
import System.IO.File as File
import System.Text.RegularExpressions as RegEx
from System.Security import Cryptography



# Key and Variables must be 16 bytes in length

def Encrypt(input_buffer, keystring, ivstring):
    key = Text.Encoding.UTF8.GetBytes(keystring)
    iv = Text.Encoding.UTF8.GetBytes(ivstring)

    algorithm = Cryptography.Aes.Create()
    transform = algorithm.CreateEncryptor(key, iv)

    output_buffer = transform.TransformFinalBlock(input_buffer, 0, input_buffer.Length)

    return output_buffer

def Decrypt(input_buffer, keystring, ivstring):
    key = Text.Encoding.UTF8.GetBytes(keystring)
    iv = Text.Encoding.UTF8.GetBytes(ivstring)

    algorithm = Cryptography.Aes.Create()
    transform = algorithm.CreateDecryptor(key, iv)

    output_buffer = transform.TransformFinalBlock(input_buffer, 0, input_buffer.Length)

    return output_buffer

def EncryptFile(filename, keystring="DEADB33FG00DB33F", ivstring="9872983742349812"):
    output_filename = filename + ".enc"
    input_buffer = File.ReadAllBytes(filename)
    encrypted_file_content = Encrypt(input_buffer, keystring, ivstring)
    File.WriteAllBytes(output_filename, encrypted_file_content)

def DecryptFile(filename, keystring="DEADB33FG00DB33F", ivstring="9872983742349812"):
    output_filename = filename + ".dec"
    input_buffer = File.ReadAllBytes(filename)
    decrypted_file_content = Decrypt(input_buffer, keystring, ivstring)
    File.WriteAllBytes(output_filename, decrypted_file_content)
