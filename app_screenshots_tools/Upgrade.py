import os
import sys
import time
import requests
from tqdm import tqdm
import win32api,ctypes,signal,getpass
import urllib3.exceptions,socket

username = getpass.getuser()
# 自定义截图保存文件夹名
make_dir = 'C:\\Users\\' + username + '\\Documents\\app_screenshots(DA)\\'
pid_path = make_dir + 'my_pid.log'

def cmd_editor_disable():
    """
    定义一个禁止cmd的快速编辑模式，防止程序挂起不执行（仅限cmd控制台使用），使用后只能爬取一次记录，不能在cmd再输入任何内容，需要重启程序
    :return:
    """
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)


def upgrade_main():
    print('\n软件正在更新中...\n')
    cmd_editor_disable()
    i = 1
    while True:
        try:
            download_url = "https://hub.fastgit.org/ld596044192/Testing-tools_scattered/releases/download/" + version + "/App." + version + ".exe"
            # print(download_url)
            print('手动更新:如果自动更新速度很慢，可以复制下面的下载地址到浏览器打开即可！\n')
            print(download_url + '\n')
            response3 = requests.get(url=download_url, timeout=10,stream=True)

            content_size = int(response3.headers['Content-Length']) / 1024
            with open("App一键截图工具" + version + ".exe", "wb") as f:
                print("文件大小为: " + str(content_size) + 'k,正在开始下载...\n')
                for data in tqdm(iterable=response3.iter_content(1024), total=content_size, unit='k',
                                 desc="App一键截图工具" + version + ".exe"):
                    f.write(data)
                print("App一键截图工具" + version + ".exe" + " 下载成功!\n")
                break
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout):
            print('第' + str(i) + '次正在重连，请耐心等待...\n')
            i += 1
            time.sleep(1)
        except ValueError:
            print('检测到你启动了代理或翻墙工具，请关闭后再继续更新！\n')
            os.system('pause')
            print('\n')
        if i > 10:
            print('下载更新失败，网络连接成功后再试！\n')
            print('3秒后自动关闭更新程序...')
            time.sleep(3)
            sys.exit()

    try:
        print('正在强制关闭旧程序...\n')
        pid = open(pid_path,'r').read()
        os.kill(int(pid),signal.SIGINT)
        time.sleep(1)
        print('正在删除旧版本...\n')
        os.remove("App一键截图工具V1.0." + str(int(version_i) - 1) + ".exe")
    except (FileNotFoundError,OSError):
        pass

    print('正在启动新版本...\n')
    time.sleep(1)
    win32api.ShellExecute(0, 'open', "App一键截图工具" + version + ".exe", '', '', 1)

    print('App一键截图工具 更新成功！\n')
    print('3秒后自动关闭更新程序！')
    time.sleep(3)
    sys.exit()


print('\nApp一键截图工具更新程序V1.0.1正式版\n')

print('正在检测新版本...\n')

while True:
    try:
        # 查看github最新版本
        response = requests.get("https://api.github.com/repos/ld596044192/Testing-tools_scattered/releases/latest")
        version = response.json()["tag_name"]
        # print(response.json()["tag_name"])
        version_i = version.split('.')[2]
        # print(version_i)
        # print('已检测到最新版本为: ' + version + '\n')
        print(version + '新版本特性及更新内容: \n')

        version_info = response.json()["body"]
        version_size = int(response.json()["assets"][0]["size"]) / 1024 / 1024
        print(version_info + '\n\n更新文件大小为' + str("%.2f " % version_size) + 'MB\n')
        break
    except ValueError:
        print('检测到你启动了代理或翻墙工具，请关闭后再继续更新！\n')
        os.system('pause')
        print('\n')
    except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError):
        print('检测更新失败，网络连接正常后再试！\n')
        print('3秒后自动关闭更新程序...')
        time.sleep(3)
        sys.exit()

while True:
    upgrade_input = input('是否更新最新版本，输入“y”进行更新，输入“n”取消更新: ').strip()
    if upgrade_input == 'y' or upgrade_input == 'Y':
        upgrade_main()
        break
    elif upgrade_input == 'n' or upgrade_input == 'N':
        print('\n3秒后自动关闭本程序！')
        time.sleep(3)
        break
    else:
        print('\n仅输入y或者n，不限大小写！请重新输入...\n')


# Github 国内镜像网站
# https://github.com.cnpmjs.org/
# https://hub.fastgit.org/ （速度快）
