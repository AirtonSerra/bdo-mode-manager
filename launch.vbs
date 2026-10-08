Option Explicit

Dim fso, shell, appFolder, pythonw, command, root, folder
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
appFolder = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = appFolder
pythonw = ""

' Instalacoes do Python Install Manager e do instalador tradicional.
For Each root In Array( _
    shell.ExpandEnvironmentStrings("%LOCALAPPDATA%\Python"), _
    shell.ExpandEnvironmentStrings("%LOCALAPPDATA%\Programs\Python"), _
    shell.ExpandEnvironmentStrings("%ProgramFiles%"))
    If fso.FolderExists(root) Then
        For Each folder In fso.GetFolder(root).SubFolders
            If LCase(Left(folder.Name, 6)) = "python" Then
                If fso.FileExists(fso.BuildPath(folder.Path, "pythonw.exe")) _
                    And fso.FolderExists(fso.BuildPath(folder.Path, "tcl")) Then
                    pythonw = fso.BuildPath(folder.Path, "pythonw.exe")
                    Exit For
                End If
            End If
        Next
    End If
    If pythonw <> "" Then Exit For
Next

If pythonw <> "" Then
    command = Quote(pythonw) & " " & Quote(fso.BuildPath(appFolder, "BDO_Mode_Manager.pyw"))
Else
    ' O launcher padrao permite localizar instalacoes em outras pastas.
    command = "pyw.exe -3 " & Quote(fso.BuildPath(appFolder, "BDO_Mode_Manager.pyw"))
End If

If WScript.Arguments.Count > 0 Then
    If WScript.Arguments(0) = "--check" Then
        WScript.Echo command
        WScript.Quit 0
    End If
End If

If Not fso.FileExists(fso.BuildPath(appFolder, "BDO_Mode_Manager.pyw")) Then
    MsgBox "Extraia todo o ZIP e mantenha o atalho junto dos arquivos do aplicativo.", 48, "BDO Mode Manager"
    WScript.Quit 1
End If

On Error Resume Next
If fso.FileExists(fso.BuildPath(appFolder, "setup_shortcuts.vbs")) Then
    shell.Run Quote(shell.ExpandEnvironmentStrings("%SystemRoot%\System32\wscript.exe")) & _
        " " & Quote(fso.BuildPath(appFolder, "setup_shortcuts.vbs")) & " --icon-only", 0, True
End If
Err.Clear
shell.Run command, 1, False
If Err.Number <> 0 Then
    MsgBox "Nao foi possivel iniciar o aplicativo. Instale Python 3 com Tkinter e o launcher do Python e tente novamente.", 48, "BDO Mode Manager"
    WScript.Quit 1
End If
On Error GoTo 0

Function Quote(value)
    Quote = Chr(34) & value & Chr(34)
End Function
