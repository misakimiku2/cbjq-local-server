' CamZoom 滚轮嗅探器 —— 普通权限启动（后台无窗口）
' 说明：如果游戏是用管理员权限跑的（启动器带 UAC），普通权限的钩子可能收不到滚轮事件，
'      那就改用 start_wheel_sniffer_admin.vbs。

Set sh = CreateObject("WScript.Shell")
sh.Run """C:\Users\MisakiMiku\.workbuddy\binaries\python\versions\3.13.12\pythonw.exe"" " & _
       """D:\test\cbjq-re\runtime\wheel_sniffer.py""", 0, False
