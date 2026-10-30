' CamZoom 滚轮嗅探器 —— 管理员权限启动（会弹一次 UAC）
' 说明：游戏若以管理员权限运行，用这个版本才能稳定收到滚轮事件。

Set sh = CreateObject("Shell.Application")
sh.ShellExecute "C:\Users\MisakiMiku\.workbuddy\binaries\python\versions\3.13.12\pythonw.exe", _
                """D:\test\cbjq-re\runtime\wheel_sniffer.py""", _
                "D:\test\cbjq-re\runtime", "runas", 0
