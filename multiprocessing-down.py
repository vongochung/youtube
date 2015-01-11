import multiprocessing,subprocess,time


def download(line):
    cli = 'youtube-dl -t http://www.youtube.com/watch?v=' + line
    subprocess.call(cli, shell=True)
    time.sleep(4)

if __name__ == '__main__':
    f = open('channel.txt','r')
    while 1:
        line = f.readline()
        if not line:break
        p = multiprocessing.Process(target=download, args=(line,))
        p.start()
    f.close()
        