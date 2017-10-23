import os
import sys
import shutil
import time


def start(src_dir, dst_dir):
    while True:
        results = [d for d in os.listdir(src_dir)]
        time.sleep(1)
        for d in results:
            d_path = os.path.join(src_dir, d)
            shutil.move(d_path, dst_dir)
        time.sleep(30)


if __name__ == '__main__':
    start(sys.argv[1], sys.argv[2])
