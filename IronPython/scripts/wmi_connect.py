import clr
clr.AddReference("System.Management")
from System.Mangement import (
    AuthenticationLevel, ImperosonationLevel, ConnectionOptions, ManagementScope
)

def authenticate():
    options = ConnectionOptions()
    options.EnablePrivilege = True
    options.Username = "administrator"
    options.Password = "secretpass123"
    network_scope = r"\\FullComputerName\root\cimv2"
    scope = ManagementScope(network_scope, options)
    print(scope)

def impersonate():
    options = ConnectionOptions()
    options.EnablePrivileges = True
    options.Impersonation = ImperosonationLevel.Impersonate
    options.Authentication = AuthenticationLevel.Default
    network_scope = r"\\FullComputerName\root\cimv2"
    scope = ManagementScope(network_scope, options)
    print(scope)