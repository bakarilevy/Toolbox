import clr
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")
import System
import System.Windows.Forms as WinForms

message = "Cancel this operation?"
caption = "Alert"
buttons = WinForms.MessageBoxButtons.YesNo
result = WinForms.MessageBox.Show(message, caption, buttons)
if result == WinForms.DialogResult.Yes:
    WinForms.MessageBox.Show("Cancelled!")
    System.Console.Write("Process Complete")
else:
    System.Console.Write("Sorry something went wrong.")