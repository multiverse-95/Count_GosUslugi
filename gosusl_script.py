import sys
import webbrowser
import os.path
import os
import time
import psutil
from subprocess import Popen, PIPE

import datetime


# Функция для получения текущего месяца
def getCurMonth():
    now = datetime.datetime.now()
    current_month = now.strftime("%m-%Y")
    return current_month


# Функция для получения текущей даты
def getCurTime():
    now = datetime.datetime.now()
    current_date = now.strftime("%d-%m-%Y")
    return current_date


# Функция для открытия сайта
def openSite():
    url = "https://www.gosuslugi.ru/"
    webbrowser.open(url)


# Функция для закрытия браузера Google Chrome
def closeBrowserChrome():
    program = "chrome.exe"
    # os.system('start /d"C:\\Program Files\\Google\\Chrome\\Application" ' + program)
    os.system("TASKKILL /F /IM " + program)


# Функция для подсчета открытий сайта Госуслуг
def writeFileCount():
    month_now = getCurMonth()  # Получаем текущий месяц
    # month_now = '07-2021'
    date_now = getCurTime()  # Получаем текущий день
    # date_now = '31-05-2021'
    file_path = fr"C:\count_gosUsl\{month_now}\{date_now}\count_gos.txt"  # Путь к файлу, куда будет сохраняться результат
    file_exist = os.path.isfile(file_path)  # Проверяем, существует ли файл
    # Если файл существует, увеличить на 1 кол-во заходов, и записать в файл
    if file_exist:
        handle = open(file_path, "r")
        data = handle.read()
        count_site = int(data)
        # print("Count old:", count_site)
        count_site += 1
        handle.close()
        with open(fr"C:\count_gosUsl\{month_now}\{date_now}\count_gos.txt", "w") as file:
            file.write(str(count_site))
            # print("WRITE SUCCESS! Count new:", count_site)
    else:  # Если файл не существует
        # print("File is not exist")
        if not os.path.exists(fr"C:\count_gosUsl\{month_now}\{date_now}"):  # Если папки с датой не существует
            if not os.path.exists(fr"C:\count_gosUsl\{month_now}"):  # Если папки с месяцем не существует
                os.mkdir(fr"C:\count_gosUsl\{month_now}")  # Создать папку с месяцем
                os.mkdir(fr"C:\count_gosUsl\{month_now}\{date_now}")  # Создать папку с датой
                with open(fr"C:\count_gosUsl\{month_now}\{date_now}\count_gos.txt",
                          "w") as file:  # Создать файл и записать туда 1
                    file.write('1')
                    # print("WRITE SUCCESS!")
            else:  # Если папка с месяцем существует
                os.mkdir(fr"C:\count_gosUsl\{month_now}\{date_now}")  # Создать папку со днем
                with open(fr"C:\count_gosUsl\{month_now}\{date_now}\count_gos.txt",
                          "w") as file:  # Записать туда файл со значением 1
                    file.write('1')
                    # print("WRITE SUCCESS!")


# Функция для получения отчета за месяц
def reportMonth():
    month_now = getCurMonth()  # Получаем текущий месяц
    sum_all_enter_gos = 0  # Счетчик для месяца
    os.chdir(fr"C:\count_gosUsl\{month_now}")  # Путь в котором будут вложенные папки
    for root, dirs, files in os.walk(".", topdown=False):  # Идем по вложенным папкам
        for name in files:
            # print(os.path.join(root, name))
            file_path = os.path.join(root, name)  # Получаем путь к файлу
            file_exist = os.path.isfile(file_path)  # Проверяем, существует ли файл
            if file_exist:  # Если файл существует
                handle = open(file_path, "r")  # Открыть файл
                data = handle.read()  # Считать данные
                count_site = int(data)  # Строку переводим в целое число
                sum_all_enter_gos += count_site  # Увеличиваем счетчик для месяца
                # print("Count old:", count_site)
    month_now = month_now + ' report'  # Названия для папки месяца
    if not os.path.exists(fr"C:\count_gosUsl\{month_now}"):  # Если папки месяца не существует
        os.mkdir(fr"C:\count_gosUsl\{month_now}")  # Создать папку с месяцем
        with open(fr"C:\count_gosUsl\{month_now}\count_month_gos.txt", "w") as file:  # Записать счетчик в файл
            file.write(str(sum_all_enter_gos))
            # print("WRITE SUCCESS!")
    else:  # Если папка с месяцем существует
        with open(fr"C:\count_gosUsl\{month_now}\count_month_gos.txt", "w") as file:  # Записать счетчик в файл
            file.write(str(sum_all_enter_gos))
            # print("WRITE SUCCESS!")
    return sum_all_enter_gos  #


# Проверяем, запущен ли процесс Google Chrome
def ifProccessRun():
    while True:  # Идем по всем запущенным процессам
        prs = Popen('tasklist', stdout=PIPE).stdout.readlines()
        pr_list = [prs[i].decode('cp866', 'ignore').split()[0] for i in range(3, len(prs))]
        # Если среди процессов есть chrome.exe
        if 'chrome.exe' in pr_list:
            x = True  # x присваем true
            break  # прерываем цикл
        else:  # Если среди процессов нет chrome.exe
            x = False  # x присваем false
            break  # прерываем цикл
    return x  # возвращаем x


# Проверяем, запущен ли процесс Google Chrome (способ 2, с использованием библиотеки psutil)
def ifProccessRun2():
    ifChrome = None
    # Идем по всем процессам
    for proc in psutil.process_iter():
        try:
            processName = proc.name()  # Получаем имя процесса
            if processName == 'chrome.exe':  # Если есть процесс chrome.exe
                ifChrome = True  # ifChrome присваиваем True
                break  # Прерываем цикл
            else:  # Если нет процесса chrome.exe
                ifChrome = False  # ifChrome присваиваем False
                continue  # Продалжаем цикл
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):  # Вызвать исключение , если что то пойдет не так
            pass
    return ifChrome  # Вернуть значение ifChrome


openSite()  # Вызвать функцию открытия файла
writeFileCount()  # Вызвать функция подсчета открытий сайта
reportMonth()  # Вызвать функцию для подсчета открытий сайта за месяц

# Код ниже позволяет определить, неактивность пользователя( т.е. если мышь не двигается, не кликается, клавиатура не используется)
if sys.platform == 'win32':
    from ctypes import *


    class LASTINPUTINFO(Structure):
        _fields_ = [('cbSize', c_uint), ('dwTime', c_int), ]


    # Функция для проверки неактивности пользователя
    def get_idle_duration():
        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = sizeof(lastInputInfo)
        if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
            millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
            return millis / 1000.0
        else:
            return 0
else:
    def get_idle_duration():
        return 0
# Пока пользователь неактивен
while True:
    if ifProccessRun2():  # Если запущен Google Chrome
        duration = get_idle_duration()  # Считаем, сколько пользователь неактивен
        print('User idle for %.2f seconds.' % duration)  # Вывести информацию, сколько пользователь неактивен
        if (duration >= 20):  # Если пользователь неактивен больше 2 минут (120 секунд)
            print('STOP')
            closeBrowserChrome()  # Закрыть браузер Google Chrome
            break  # Прервать цикл
        else:  # Иначе прибавлять по секунде
            time.sleep(1)
    else:  # Если пользователь закрыл браузер Google Chrome
        print('Proccess stopped by user')
        break
