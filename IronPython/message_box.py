import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox, MessageBoxButtons

MessageBox.Show("Hello From IronPython", "IronPy", MessageBoxButtons.OKCancel)