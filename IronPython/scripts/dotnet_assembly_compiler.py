from System.Environment import CurrentDirectory
from System.IO import Path, Directory

from System.CodeDom import Compiler
from Microsoft.CSharp import CSharpCodeProvider
from Microsoft.VisualBasic import VBCodeProvider


# code = Source code to compile as a string
# name = Name of assembly to generate
# references = List of assemblies needed (IE. assemblies not part of the .NET Framework)
# outputDir = Location to save output assembly
# inMemory = Returns the assembly or location assemly was saved at if inMemory is set to false
# csharp = Assumes you are providing C# code if not VB compiler is used

def Generate(code, name, references=None, outputDir=None, inMemory=False, csharp=True):
    params = Compiler.CompilerParameters()

    if not inMemory:
        if outputDir is None:
            outputDir = Directory.GetCurrentDirectory()
        asmPath = Path.Combine(outputDir, name + ".dll")
        params.OutputAssembly = asmPath
        params.GenerateInMemory = False
    else:
        params.GenerateInMemory = True
    params.TreatWarningsAsErrors = False
    params.GenerateExecutable = False
    params.CompilerOptions = "/optimize"

    for reference in references or []:
        params.ReferencedAssemblies.Add(reference)
    
    if csharp:
        provider = CSharpCodeProvider()
    else:
        provider = VBCodeProvider()
    compile = provider.CompileAssemblyFromSource(params, code)

    if compile.Errors.HasErrors:
        errors = list(comile.Errors.List)
        raise Exception("Compile error: %r" % errors)
        
    if inMemory:
        return compile.CompiledAssembly
    return compile.PathToAssembly