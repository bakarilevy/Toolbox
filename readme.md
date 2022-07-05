# The Toolbox

- Recon
- Enumeration
- Exploitation
- Persistence
- Forensics

## Recon

### Finding Emails
hunter.io
phonebook.cz
clearbit (Chrome Extension)

### Breached Credentials
Credential Stuffing

### Hunting Subdomains
crt.sh (This website can be used for certificate fingerprinting)
To use a wildcard on that site for search with the follwoing format:
```
%.target.com
```

We can use the sublist3r tool for domain discovery.
```
sublist3r -d <target.com>
```

OWASP Amass can also be used.

### Geoint
geoguesser

### Email Discovey
Search plaforms:
```
hunter.io
phonebook.cz
clearbit (chrome only)
```
Email verification:
```
verifyemailaddress.io
email-checker.net/validate
```
Don't underestimate "forgot passwords"

### Password Discovery
```
dehashed
weleakinfo
leakcheck
snusbase
haveibeenpwned
scylla.sh
hashes.org
```

### Username Discovery
```
namechk.com
```
### Person Discovery
```
whitepages.com
truepeoplesearch.com
fastpeoplesearch.com
thatsthem.com
pimeye
tineye
```

### Voter Records
```
voterrecords.com
```

## Networking Commands

Shows your different interface types and IP addresses associated with them.
```
ifconfig
```
The newer command to replace ifconfig is now ip
```
ip a (ifconfig)
ip n (arp table)
ip r (routing table)
```
For wireless
```
iwconfig
```
Used to test connectivity between hosts.
```
ping <addr>
```
IP address and MAC address associated with it.
```
arp -a
```
Displays active connections on your machine.
```
netstat -ano
```
Displays routing table along with default gateway.
```
route
```

LM Hash for Pass the Hash attacks on Windows
```
aad3b435b51404eeaad3b435b51404ee
```

You can try to kill the Windows Defender process MsMpEng.exe

## Phishing

- Gophish

Username is admin password is gophish
We will want to run the Gophish Framework on a cloud environment so we can resolve DNS requests to it rather than running it locally.
We can use a platform like Digital Ocean, Heroku, or Oracle Cloud for this.
We can use a site like freenom.com to get a free domain name, but its best to use a provider as close to your target as possible.
After you have your domain, be sure to point it to the name servers of your cloud platform, IE on freenom you would need to point to the digital ocean nameservers if you were using both of those.

```
ns1.digitalocean.com
ns2.digitalocean.com
```
For your VPS provider create a CNAME dns record for www (should be @ or hostname)

It may take some time to propogate the domain name servers so maybe give it 24 hours to see if your phishing server is tied to your domain.
To check your DNS and see what IP address it is using go to:
```
intodns.com/mydomain.us
```

On our VPS server we should install the screen package, after running the gophish binary we should run Ctrl-A and then D this should keep the process running detached even if we logout of the ssh session.

Once you have your domain setup, you may need to find a way to allow your cloud provider to unlock your smtp server.

The next thing we need is to set up an SSL certificate for our server so users can connect over https.

If we go to zerossl.com we can get a free LetsEncrypt certificate.
We will select the options DNS Verification and Accept Let's Encrypt SA.
Make sure to download the CSR and account key.
After we have generated these files and certificates, we will need to add some
Domain TXT records on our VPS dashboard.

After this we will download the domain certificate and key. Not the same as above.
You will send these files to the phishing server and change the gophish config file to the appropriate path to the certificate and key files.

We will also need an SMTP server that allows you to spoof such as SMTP to go.

## Infrastructure

Using Nginx Web Server for standing up C2 infrastructure.
Manual setup configuration is as follows...
Install with the following commands:
```
sudo apt-get install -y nginx
sudo vi /etc/nginx/conf.d/reverse.conf
```
See the example of reverse.conf in the Infrastructure directory for configuration.
Once configured setup SSL certificates using Let's Encrypt:
```
add-apt-repository ppa:certbot/certbot
apt-get update && apt-get install python-certbot-nginx
sudo certbot --nginx -d mydomain.com -d www.mydomain.com
```

To setup Docker run the following:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository "deb[arch=amd64] https://download.docker.com/ubuntu $(lsb_release -cs) stable"

apt update
apt install -y docker-ce
```

Once setup we can pull down Metasploit:
```
docker pull phocean/msf

docker run --rm -it phocean/msf
```

--rm flag deletes the container on termination, and -it makes terminal interactive.

Boot Up:
```
./msfconsole
```

We can tell Docker to map packets and folders from the host to the container:

```
sudo docker run --rm -it -p8400-8500:8400-8500 -v ~/.msf4:/root/.msf4 -v /tmp/msf:/tmp/data
```

An example Dockerfile for SILENTTRINITY can be seen in the infrastructure folder.

And of course we can build our container:
```
docker build -t silent .
```

We can run the container in the background with the following:
```
docker run -d -v /opt/st:/root/st/data -p5000:5000
```

Using a Docker Hub account you can push your container image:
```
docker login

docker tag <image-name> <username/repo-name>
docker push <username/repo-name>
```

We can then docker pull our image to any machine with Docker installed!

We can also dockerize the Nginx server for routing C2 traffic.
With that done a one liner can be used to spin up the Nginx server.
```
docker run -d -p80:80 -p443:443 -e DOMAIN="www.somedomain.com" -e C2IP="192.168.1.29" -v /opt/letsencrypt:/etc/letsencrypt <username>/nginx
```
Keep in mind the DNS record for "somedomain.com" should point to the Nginx server's public IP.
The SILENTRINITY and Metasploit containers can run on the same host however, Nginx must run on a different host.
It is likely the first to get an IP ban.
Anytime it goes down, running that command again we have a new domain and IP.
It would be smart to purchase a couple of legit domains as well, one for user workstations, and one for servers.
Ex: experienceyoufood.com V.S. linux-packets.org

Lets automate the last piece of infrastructure setup.
Acquire a credit card and get access to AWS.
On our bounce server lets intall Terraform executing the following:
```
wget https://releases.hashicorp.com/terraform/0.12.12/terraform_0.12.12_linux_amd64.zip

unzip terraform_0.12.12_linux_amd64.zip

chmod +x terraform
```

In the AWS IAM (User mangement service) we need to create a programmitic account
and grant full access to EC2 operations.
Don't forget to keep the AWS Access Key ID and the Secret Access Key!
We will then install the awscli tool and store the credentials:
```
sudo apt install awscli

aws configure
AWS ACCESS KEY ID: <access-key-id>
AWS SECRET ACCESS KEY: <secret-access-key>
Default region name: eu-west-1

mkdir infra && cd infra
```
We setup the main.tf and provider.tf
Provider initializes the AWS connector, loads credentials, and assigns a default region.
In Main we create a resource, which is an atomic unit of a cloud provider service.
Be that a Server, SSH key, Firewall, etc. 
The granularity depends on the service provider.
Terraform spawns the server after we define the aws_instance as a resource.
The "ami-0039c41a10b230acb" in our basic resource is an Amazon Machine Image identfied as an Ubuntu 18.04 server.
Now we can initialize:
```
terraform init
```
We can then stage our changes and see the output in formatted json:
```
terraform fmt && terraform plan
```
If we are happy with our changes we can run:
```
terraform apply
```
This deploys the server to AWS.
If we want to launch more servers we can simply add a count variable in main.tf
```
count = 10
instance_type = "t2.micro"
```

After we apply our Terraform changes then we should be able to SSH into our new ec2 instances:
```
ssh -i .ssh/id_rsa ubuntu@<cloud-ip-addr>
```
And if we run:
```
docker ps
```
We should see that we have our image installed.

The scaffold for our attack infrastructure is relatively complete, with this we can spin up new infrastructure in seconds.

## StandardPython
Compiling a python binary using nuitka is quite simple
```
python -m nuitka --onefile windows.py
```
To solve the error:
```
Nuitka-Scons:INFO: Backend C compiler: gcc (gcc).
collect2: fatal error: ld terminated with signal 11 [Segmentation fault]                              
compilation terminated. Error 1
```
Try running:
```
python3 -m nuitka --lto=no windows.py
```

## IronPython

Loading .NET Assemblies in memory from Powershell:
```
$directorypath = (Get-Item .).FullName
$assemblypath = $directorypath + "\program.dll"
$bytes = [System.IO.File]::ReadAllBytes($assemblypath)
$assembly = [System.Reflection.Assembly]::Load($bytes)
$entryPointMethod = $assembly.GetTypes().Where({ $_.Name -eq 'Program' }, 'First').GetMethod('Main', [Reflection.BindingFlags] 'Static, Public, NonPublic')
$entryPointMethod.Invoke($null, (, [string[]] ($null)))
```

With pyc.py you can create console or Windows Assemblies from python scripts.
Basic usage looks like this:
```
ipyc /out:myprogram.exe /main:mainfile.py /target.exe program.py support.py
```

To create a standalone executable you will need to compile with the command:
```
ipyc /target:winexe /embed /standalone /main:program.py
```

The above will generate an assembly called myprogram.exe (/out) which is a console app (/target) and will execute the code in mainfile.py first (/main) and will also include code from program.py and support.py in the assembly.

You can also perform static compilation of a .NET assembly using IronPython iteslf:
```py
import clr
# Assembly Name, File names, Key Word Arguments
clr.CompileModules("ipy_modules.dll", "module1.py", "module2.py")
```

Now we can import and use these modules:
```py
import clr
clr.AddReference("ipy_modules.dll")
import module1, module2
```

CompileModules also takes a keyword mainModules argument that specifies the python file that acts as the entry point for the application.

C# Class Library for IronPython example:
```c#
using System;
using System.Collections;

namespace PythonExtension
{
    public delegate int Callback(int input);

    public class PythonClass : IEnumerable //This class implements IEnumerable
    {
        private int _value;
        private Callback _callback;

        public PythonClass(int value, Callback callback) // Constructor takes a callback value
        {
            _value = value;
            _callback = callback;
        }

        public override string ToString() // Used for String representation
        {
            return String.Format("PythonClass<{0}>", _value);
        }

        public IEnumerator GetEnumerator() //Used for Iteration
        {
            for (int i = _value; i > 0; i--)
            {
                if (i % 2 == 0) {
                    yield return callback(i);
                }
            }
        }

        public static PythonClass operator + (PythonClass a, PythonClass, b) // Operator Overloading for addition
        {
            return new PythonClass(a._value + b._value, a.callback);
        }

        public Object this[Object index] {
            get {  // Equivalent of Python __getitem__
                Console.WriteLine("Indexed with {0}", index);
                return index;
            }
            set {  // Equivalent of Python __setitem__
                Console.WriteLine("Index {0} set to {1}", index, value);
            }
        }
    }
}
```

P/Invoke Wrapper:
```c#
using System;
using System.Text;
using System.Runtime.InteropServices;

namespace WindowsUtils
{
    public class WindowsUtils
    {
        [DllImport("user32.dll")]
        public static extern bool IsWindowVisible(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr GetTopWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindow(IntPtr hWnd, uint wCmd);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowTextLength(IntPtr hWnd);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowText(IntPtr hWnd, [Out] StringBuilder lpString, int nMaxCount);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetClassName(IntPtr hWnd, [Out] StringBuilder lpString, int nMaxCount);
    }
}
```

Using the dotnet_assembly_compiler.py script you can load the above WindowsUtil class into memory:
```py
import clr
assembly = Generate(source, "WindowsUtils", inMemory=True)
clr.AddReference(assembly)
from WindowsUtils import WindowsUtils
```
We can also do:
```py
assembly = Generate(source, "WindowsUtils", inMemory=True)
WindowsUtils = assembly.WindowsUtils.WindowsUtils
```


### Embedding IronPython

To embed the IronPython Engine into a .NET assembly we need to include the 5 assemblies that come with it:

- Microsoft.Scripting.dll
- Microsoft.Scripting.Core.dll
- IronPython.dll
- IronPython.Modules.dll
- Microsoft.Scripting.ExtensionAttribute.dll

The first two assemblies are part of the Dynamic Language Runtime, the next two are part of IronPython.
The final assembly is used so that .NET projects using .NET 2.0 and 3.0 can use IronPython.
It must be included in the project but does not need to be referenced.
The main entrypoint for apps embedding IronPython is the Python class in the IronPython Hosting namespace.

#### Embedding IronPython script into C# Portable Executable

Setting up an IronPython engine in C#:
```c#
using IronPython.Hosting;

ScriptEngine engine = Python.CreateEngine();
```
The Dynamic Language Runtime supports creating multiple runtimes in a single application, allowing for context execution segmented
from each other.
We need to use both the ScriptSource and ScriptScope APIs from the Hosting API to run a python script.

Execute IronPython code from a string in C#:
```c#
ScriptSource source;
source = engine.CreateScriptFromString(sourceCode, SourceCodeKind.Statements);
ScriptScope scope = engine.CreateScope();
source.Execute(scope);
```

Execute IronPython code from a file in C#:
```c#
ScriptSource source;
source = engine.CreateScriptFromFile(path);
ScriptScope scope = engine.CreateScope();
source.Execute(scope);
```

We can also set the command line arguments for a script like this:
```c#
using IronPython.Runtime;

List argList = new List();
argList.extend(args);
ScriptScope sys = Python.GetSysModule(engine);
sys.SetVariable("argv", argList);
```

We will also need to set the module search path properly for import statements during embedding.
```c#
string filename = "program.py";
string path = Assembly.GetExecutingAssembly().Location;
string rootDir = Directory.GetParent(path).FullName;

List<string> paths = new List<string>();
paths.Add(rootDir);

string path = Environment.GetEnvironmentVariable("IRONPYTHONPATH");
if (path != null && path.Length > 0) {
    string[] items = path.Split(";");
    foreach (string p in items) 
    {if (p.Length > 0) { paths.Add(p); }}
}
engine.SetSearchPaths(paths.ToArray());
```

Lets catch any exceptions from IronPython execution without it being fatal to the C# app:
```c#
try {
    ScriptSource source;
    source = engine.CreateScriptSourceFromFile(path);
    int result = source.ExecuteProgram();
    return result
}

catch (Exception e)
{
    ExceptionOperations eo = engine.GetService<ExceptionOperations>();
    Console.Write(eo.FormatException(e));
    return 1;
}
```

#### Embedding IronPython as a scripting engine in C# Application

Lets begin with getting and setting variables from a scope.

Creating an execution scope C#:
```c#
public class Engine
{
    ScriptEngine _engine;
    ScriptRuntime _runtime;
    CompiledCode _code;
    ScriptScope _scope;

    //_runtime.LoadAssembly(typeof(String).Assembly);

    public class Engine(string source)
    {
        _engine = Python.CreateEngine();
        _runtime = engine.Runtime;
        _scope = _engine.CreateScope();
        _scope.SetVariable("__name__", "__main__");
        
        ScriptSource _script = _engine.CreateScriptFromString(source, SourceCodeKind.Statements);
        _code = _script.Compile();
    }

    public bool Execute()
    {
        try
        {
            _code.Execute(_scope);
            return true;
        }
        catch (Exception e)
        {
            ExceptionOperations eo = _engine.GetService<ExceptionOperations>();
            Console.Write(eo.FormatException(e));
            return false;
        }
    }

    public void SetVariable(string name, object value)
    {
        _scope.SetVariable(name, value);
    }

    public bool TryGetVariable(string name, out result)
    {
        return _scope.TryGetVariable(name, out result);
    }
}
```

Retrieving embedded resource from an assembly:
```c#
static string GetSourceCode()
{
    Assembly assembly = Assembly.GetExecutingAssembly();
    string name = "BasicEmbedding.source_code.py";
    Stream stream = assembly.GetManifestResourceStream(name);
    StreamReader textStreamReader = new StreamReader(stream);
    return textStreamReader.ReadToEnd();
}
```

