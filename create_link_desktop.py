import os, winshell
from win32com.client import Dispatch

# Создание ярлыка на рабочем столе

# Получаем путь до рабочего стола.
desktop = winshell.desktop()
# Соединяем пути, с учётом разных операционок.
path = os.path.join(desktop, "ГОСУСЛУГИ.lnk")
# Задаём путь к файлу, к которому делаем ярлык.
target = r"D:\Documents\Test_SITE\Start_Count_Gos.bat"
# Назначаем путь к рабочей папке.
wDir = r"D:\Documents\Test_SITE"
# Путь к нужной нам иконке.
icon = r"D:\Documents\Test_SITE\gosusl.ico"
# С помощью метода Dispatch, обьявляем работу с Wscript (работа с ярлыками, реестром и прочей системной информацией в windows)
shell = Dispatch('WScript.Shell')
# Создаём ярлык.
shortcut = shell.CreateShortCut(path)
# Путь к файлу, к которому делаем ярлык.
shortcut.Targetpath = target
# Путь к рабочей папке.
shortcut.WorkingDirectory = wDir
# Берем иконку.
shortcut.IconLocation = icon
# Обязательное действие, сохраняем ярлык.
shortcut.save()