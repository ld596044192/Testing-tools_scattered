import subprocess, re, os, time, getpass,sys

username = getpass.getuser()
# 自定义截图保存文件夹名
dirname = '1'
make_dir = 'C:\\Users\\' + username + '\\Documents\\app_screenshots(DA)\\'
count_path = make_dir + 'screenshots_count.txt'
save_path = 'C:\\Users\\' + username + '\\Desktop\\' + dirname + '\\'
model_path = make_dir + 'screenshots_model.txt'


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


version_path = resource_path(os.path.join('doc','app_screenshot_version.txt'))


def execute_cmd(cmd):
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
    proc.stdin.close()
    proc.wait()
    result = proc.stdout.read().decode('gbk') # 注意你电脑cmd的输出编码（中文是gbk）
    proc.stdout.close()
    return result


def version_history_new():
    print('###############################\n')
    print('欢迎使用App一键截图工具，使用前请确保计算机存在ADB服务，否则会闪退！\n')
    print('V1.0.4版本更新:')
    print('1.大大地优化了代码\n2.新增清屏功能（防止大量信息干扰，因人而异）(New)\n3.优化完善文字显示提示\n4.新增安全模式（解决“截图无法截取完整”的问题）(New)\n'
          '5.修复了截图截取不完整的BUG（尤其是截图文件比较大的情况）\n\nBy 李达\n')
    print('###############################')


def version_history_hidden():
    version_fp = open(version_path,'r',encoding='utf-8').read()
    print(version_fp)


def readme():
    print('\nヽ(✿ﾟ▽ﾟ)ノ 截图工具输入指令说明:')
    print('（1）模式切换说明: 输入M切换到 自动模式（自动点亮设备屏幕）；输入F切换到 快捷模式(不自动点亮设备屏幕)；不限大小写！')
    print('（2）版本历史记录查看说明: 输入H显示版本历史记录（不限大小写!）')
    print('（3）清空记录说明: 输入cls或clear清空所有显示的截图信息记录，但不会清空本地缓存的截图文件（不限大小写!）')
    print('（4）安全模式切换说明: 输入S切换到 安全模式（切换到该模式即可解决“截图无法截取完整”的问题）（不限大小写!）\n')


version_history_new()
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

            devices_fp = execute_cmd('adb devices -l')
            # devices_read = devices_fp.read()
            devices_re = re.findall('\\n(.*?)\\sdevice', devices_fp)
            if not devices_re:
                print('\n设备没有连接！请连接设备后再截图！\n')
            else:
                screenshots()
        except EOFError:
            pass
