import vt_download
import sys
import os


def get_sha1(sha1_file):
    sha1s = []
    with open(sha1_file, 'r') as f:
        for line in f:
            sha1 = line.strip()
            sha1s.append(sha1)
    return sha1s

def get_name(dir):
    name = []
    for file in os.listdir(dir):
        if os.path.isfile(file):
            name.append(file)
    return name

def download(sha1s, download_dir, exist_dir):
    vt_query = vt_download.VT_Download()
    exist_files = get_name(exist_dir)
    for sha1 in sha1s:
        if sha1 in exist_files:
            continue
        try:
            content = vt_query.download(sha1)
            if content != None:
                file_path = os.path.join(download_dir, sha1)
                with open(file_path, 'wb') as f:
                    f.write(content)
        except:
            print sha1


def main():
    download(get_sha1(sys.argv[1]), sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()