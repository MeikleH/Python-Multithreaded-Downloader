import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# 创建一个锁对象和一些全局变量
lock = threading.Lock()
current_size = 0
last_time = time.time()


def calc_divisional_range(filesize, chuck=10):
    """
    计算文件下载的分段范围

    :param filesize: 文件的总大小
    :param chuck: 分段的数量
    :return: 返回一个列表，列表中的每个元素是一个包含两个元素的列表，表示一个下载分段的开始和结束位置
    """
    step = filesize // chuck
    arr = list(range(0, filesize, step))
    result = []
    for i in range(len(arr) - 1):
        s_pos, e_pos = arr[i], arr[i + 1] - 1
        result.append([s_pos, e_pos])
    result[-1][-1] = filesize - 1
    return result


def range_download(save_name, s_pos, e_pos):
    """
    下载指定范围的文件内容，并将其写入到本地文件

    :param save_name: 本地文件的名称
    :param s_pos: 下载范围的开始位置
    :param e_pos: 下载范围的结束位置
    """
    global current_size, last_time
    headers = {"Range": f"bytes={s_pos}-{e_pos}"}
    res = requests.get(url, headers=headers, stream=True)
    with open(save_name, "rb+") as f:
        f.seek(s_pos)
        for chunk in res.iter_content(chunk_size=64 * 1024):
            if chunk:
                f.write(chunk)
                # 更新已下载的大小，并记录更新时间
                with lock:
                    current_size += len(chunk)
                    last_time = time.time()


def show_progress(filesize: int, interval: int = 1):
    """
    显示下载进度和速度

    :param filesize: 文件的总大小
    :param interval: 显示进度的间隔时间，单位为秒
    """
    global current_size, last_time
    old_size = 0
    old_time = last_time
    while True:
        with lock:
            completed = current_size
            current_time = last_time
        progress = completed / filesize
        # 计算下载速度
        delta_size = completed - old_size
        delta_time = current_time - old_time
        if delta_time > 0:
            speed = delta_size / delta_time
        else:
            speed = 0
        print(f"下载进度：{progress * 100:.2f}%，速度：{speed / 1024:.2f}KB/s")
        old_size = completed
        old_time = current_time
        if completed >= filesize:
            break
        time.sleep(interval)

if __name__ == '__main__':

    url = "https://releases.ubuntu.com/22.04.2/ubuntu-22.04.2-desktop-amd64.iso"
    res = requests.head(url)
    filesize = int(res.headers['Content-Length'])
    divisional_ranges = calc_divisional_range(filesize)

    save_name = "ubuntu-22.04.2-desktop-amd64.iso"
    # 先创建空文件
    with open(save_name, "wb") as f:
        pass
    with ThreadPoolExecutor() as p:
        futures = []
        for s_pos, e_pos in divisional_ranges:
            print(s_pos, e_pos)
            futures.append(p.submit(range_download, save_name, s_pos, e_pos))
        # 在所有下载任务提交后，提交显示进度的任务
        progress_future = p.submit(show_progress, filesize)
        # 等待所有下载任务执行完毕
        as_completed(futures)
        # 等待显示进度的任务
        progress_future.result()
