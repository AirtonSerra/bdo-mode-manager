Option Explicit

Dim fso, shell, appFolder, iconFolder, iconSource, iconPath, shortcut, desktopFolder
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
appFolder = fso.GetParentFolderName(WScript.ScriptFullName)
iconSource = fso.BuildPath(appFolder, "assets\bdo-mode-manager-spirit-outline.ico")
If Not fso.FileExists(iconSource) Or Not fso.FileExists(fso.BuildPath(appFolder, "launch.vbs")) Then
    MsgBox "Extraia todo o ZIP antes de configurar os atalhos.", 48, "BDO Mode Manager"
    WScript.Quit 1
End If

iconFolder = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%\BDOModeManager")
If Not fso.FolderExists(iconFolder) Then fso.CreateFolder iconFolder
iconPath = fso.BuildPath(iconFolder, "app.ico")
fso.CopyFile iconSource, iconPath, True

If WScript.Arguments.Count > 0 Then
    If WScript.Arguments(0) = "--icon-only" Then WScript.Quit 0
End If

desktopFolder = shell.SpecialFolders("Desktop")
Set shortcut = shell.CreateShortcut(fso.BuildPath(desktopFolder, "BDO Mode Manager.lnk"))
shortcut.TargetPath = shell.ExpandEnvironmentStrings("%SystemRoot%\System32\wscript.exe")
shortcut.Arguments = Quote(fso.BuildPath(appFolder, "launch.vbs"))
shortcut.WorkingDirectory = appFolder
shortcut.IconLocation = iconPath & ",0"
shortcut.Description = "BDO Mode Manager"
shortcut.Save

If WScript.Arguments.Count = 0 Then
    MsgBox "Icone configurado e atalho criado na area de trabalho. Use BDO Mode Manager para abrir o aplicativo. Se mover a pasta, execute esta configuracao novamente.", 64, "BDO Mode Manager"
End If

Function Quote(value)
    Quote = Chr(34) & value & Chr(34)
End Function
