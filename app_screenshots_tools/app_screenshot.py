import socket
import subprocess, re, os, time, getpass,sys
import requests,win32api
import urllib3.exceptions

username = getpass.getuser()
# 自定义截图保存文件夹名
dirname = 'App截图文件夹（DA）'
make_dir = 'C:\\Users\\' + username + '\\Documents\\app_screenshots(DA)\\'
count_path = make_dir + 'screenshots_count.txt'
save_path = 'C:\\Users\\' + username + '\\Desktop\\' + dirname + '\\'
model_path = make_dir + 'screenshots_model.txt'
upgrade_close = make_dir + 'upgrade_log.log'
pid_path = make_dir + 'my_pid.log'
# 设置本程序版本信息
version_name = 'V1.0.6'
version_code = 106


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


version_path = resource_path(os.path.join('doc','app_screenshot_version.txt'))
version_path_new = resource_path(os.path.join('doc','app_screenshot_new.txt'))
upgrade_path = resource_path(os.path.join('upgrade','Upgrade.exe'))


def execute_cmd(cmd):
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
    proc.stdin.close()
    proc.wait()
    result = proc.stdout.read().decode('gbk') # 注意你电脑cmd的输出编码（中文是gbk）
    proc.stdout.close()
    return result


def version_history_new():
    version_new = open(version_path_new,'r',encoding='utf-8').read()
    print(version_new)


def version_history_hidden():
    version_fp = open(version_path,'r',encoding='utf-8').read()
    print('\n' + version_fp + '\n')


def readme():
    print('\nヽ(✿ﾟ▽ﾟ)ノ 截图工具输入指令说明:')
    print('（1）模式切换说明: 输入M切换到 自动模式（自动点亮设备屏幕）；输入F切换到 快捷模式(不自动点亮设备屏幕)；不限大小写！')
    print('（2）版本历史记录查看说明: 输入H显示版本历史记录（不限大小写!）')
    print('（3）清空记录说明: 输入cls或clear清空所有显示的截图信息记录，但不会清空本地缓存的截图文件（不限大小写!）')
    print('（4）安全模式切换说明: 输入S切换到 安全模式（切换到该模式即可解决“截图无法截取完整”的问题）（不限大小写!）')
    print('（5）自动更新启动说明: 输入yy可以开启自动更新提示（每次打开工具都会自动检测一次更新）（不限大小写!）')
    print('（6）手动检查更新启动说明: 输入y可以进行手动检测更新（当关闭自动更新提示时很有用）（不限大小写!）\n')


def version_upgrade():
    upgrade_read = open(upgrade_close,'r').read()
    if upgrade_read == 'close':
        pass
    else:
        try:
            # 查看github最新版本
            print('\n正在检查新版本...\n')
            response = requests.get("https://api.github.com/repos/ld596044192/Testing-tools_scattered/releases/latest")
            version = response.json()["tag_name"]
            version_split = ''.join(version.split('V')).split('.')
            version_finally = ''.join(version_split)
            version_size = int(response.json()["assets"][0]["size"]) / 1024 / 1024
            if version_code < int(version_finally):
                print('已检测到最新版本为: ' + str(version) + '  更新的文件大小为' + str("%.2f " % version_size) + 'MB\n')
                while True:
                    upgrade_input = input('是否更新最新版本，输入“y”进行更新，输入“n”取消更新，关闭自动更新提示请输入“nn”: ').strip()
                    if upgrade_input == 'y' or upgrade_input == 'Y':
                        win32api.ShellExecute(0, 'open', upgrade_path, '', '', 1)
                        print('\n开始更新本程序（更新完毕前仍可使用本程序）...\n')
                        # print('3秒后自动关闭本程序...')
                        # time.sleep(3)
                        # sys.exit()
                        break
                    elif upgrade_input == 'n' or upgrade_input == 'N':
                        break
                    elif upgrade_input == 'nn' or upgrade_input == 'NN':
                        with open(upgrade_close, 'w') as fp:
                            fp.write('close')
                        print('\n已关闭自动更新提示！\n')
                        break
                    else:
                        print('\n仅输入y或者n或者nn，不限大小写！请重新输入...\n')
        except (socket.gaierror,urllib3.exceptions.NewConnectionError,urllib3.exceptions.MaxRetryError,
                requests.exceptions.ConnectionError):
                print('检测更新失败，网络连接正常后再试！')
        else:
            print('你目前是最新版本，无需更新！\n')


if not os.path.exists(upgrade_close):
    with open(upgrade_close,'w') as fp:
        fp.write('')
elif not os.path.exists(pid_path):
    with open(pid_path,'w') as fp:
        fp.write('')
my_pid = os.getpid()
with open(pid_path, 'w') as fp:
    fp.write(str(my_pid))
version_history_new()
version_upgrade()
readme()


def screentshots_main(f):
    model_read_2 = open(model_path, 'r').read()
    model_finally = model_read_2.split(' ')[0]
    execute_cmd('adb shell screencap -p /sdcard/da_screenshots/test' + str(f) + '.png')
    print('\n正在截图...\n')
    if model_finally == 'S':
        time.sleep(2)
    else:
        time.sleep(1)
    execute_cmd('adb pull /sdcard/da_screenshots/test' + str(f) + '.png C:\\Users\\' + username + '\\Desktop\\' + dirname)
    print('截图成功！路径保存在: C:\\Users\\' + username + '\\Desktop\\' + dirname + '\\test' + str(f) + '.png\n')
    with open(count_path, 'w') as fp:
        fp.write(str(f))


def screentshots_model(f):
    model_read_2 = open(model_path, 'r').read()
    model_finally = model_read_2.split(' ')[0]
    # print(model_finally)
    if model_finally == 'M':
        print('\n正在自动点亮屏幕...')
        execute_cmd('adb shell input keyevent 224')
        time.sleep(2)
        screentshots_main(f)
    else:
        screentshots_main(f)
    # 删除截图缓存（减少占用空间）
    execute_cmd('adb shell rm -r /sdcard/da_screenshots/test' + str(f) + '.png')


def screenshots():
    command1 = 'adb shell cd /sdcard/da_screenshots'
    p1 = subprocess.Popen(command1, shell=False, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
    while p1.poll() is None:
        f = int(open(count_path, 'r').read())
        f += 1
        line1 = p1.stdout.readline().decode('utf8').split(':')[(-1)].split()
        line_1 = ' '.join(line1)
        # print(line_1)
        if line_1 == 'No such file or directory':
            os.popen('adb shell mkdir /sdcard/da_screenshots', 'r')
            screentshots_model(f)
        elif not os.path.exists(save_path):
            os.makedirs(save_path)
        else:
            screentshots_model(f)


def txt_write():
    with open(count_path, 'w') as fp:
        fp.write('0')
    with open(model_path, 'w') as fp:
        fp.write('F 快捷模式(不自动点亮设备屏幕)')
    print('程序初始化完成！\n')


while True:
    if not os.path.exists(make_dir) and not os.path.exists(save_path):
        print('\n首次使用程序需要初始化，程序正在初始化...\n')
        os.makedirs(make_dir)
        os.makedirs(save_path)
        txt_write()
    elif os.path.exists(make_dir) and not os.path.exists(save_path):
        print('\n首次使用程序需要初始化，程序正在初始化...\n')
        os.makedirs(save_path)
        txt_write()
    elif not os.path.exists(make_dir) and os.path.exists(save_path):
        print('\n首次使用程序需要初始化，程序正在初始化...\n')
        os.makedirs(make_dir)
        txt_write()
    else:
        model_read = open(model_path,'r').read()
        # print(model_read)
        model_finally1 = model_read.split(' ')[0]
        model_finally2 = model_read.split(' ')[1]
        try:
            screenshot = input('直接敲击回车键即可进行截图！(当前模式: ' + model_finally2 + ')').strip()
            if screenshot == 'M' or screenshot == 'm':
                with open(model_path, 'w') as fp:
                    fp.write('M 自动模式（自动点亮设备屏幕）')
                    model_read = open(model_path, 'r').read()
                time.sleep(0.5)
                model_read_1 = open(model_path, 'r').read()
                model_finally2 = model_read_1.split(' ')[1]
                print('\n当前模式已切换为 ' + model_finally2 + '\n')
                continue
            elif screenshot == 'F' or screenshot == 'f':
                with open(model_path, 'w') as fp:
                    fp.write('F 快捷模式(不自动点亮设备屏幕)')
                    time.sleep(0.5)
                model_read_1 = open(model_path, 'r').read()
                model_finally2 = model_read_1.split(' ')[1]
                print('\n当前模式已切换为 ' + model_finally2 + '\n')
                continue
            elif screenshot == 'S' or screenshot == 's':
                with open(model_path, 'w') as fp:
                    fp.write('S 安全模式(可解决截图截取不完整的问题哦~)')
                    time.sleep(0.5)
                model_read_1 = open(model_path, 'r').read()
                model_finally2 = model_read_1.split(' ')[1]
                print('\n当前模式已切换为 ' + model_finally2 + '\n')
                continue
            elif screenshot == 'H' or screenshot == 'h':
                version_history_hidden()
                continue
            elif screenshot == 'cls' or screenshot == 'CLS' or screenshot == 'clear' \
                or screenshot == 'CLEAR':
                clear = os.system('cls')
                version_history_new()
                readme()
                continue
            elif screenshot == 'yy' or screenshot == 'YY':
                with open(upgrade_close,'w') as fp:
                    fp.write('')
                    print('\n自动更新提示已开启，下次启动生效！\n')
                continue
            elif screenshot == 'y' or screenshot == 'Y':
                version_upgrade()
                continue

            devices_fp = execute_cmd('adb devices -l')
            # devices_read = devices_fp.read()
            devices_re = re.findall('\\n(.*?)\\sdevice', devices_fp)
            if not devices_re:
                print('\n设备没有连接！请连接设备后再截图！\n')
            else:
                screenshots()
        except EOFError:
            pass
