Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\hejia\.gemini\config\skills\easyeda-api"
WshShell.Run """E:\Tools\Nodejs\node.exe"" ""C:\Users\hejia\.gemini\config\skills\easyeda-api\scripts\bridge-server.mjs""", 0, False
