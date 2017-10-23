#-*- coding: UTF-8 -*-

import os, sys
import requests


url = 'https://www.virustotal.com/vtapi/v2/file/download'
#VTKey = "1d3b13007f0f9db1c140ef079ce9f526308856a214e3e46826bf425d5acd9bed"
#VTKey = "f65e2f517a8ef3d4d95e2bd20a600c47ff811efb63e431100def56421e607aff"
VTKey = "f556c7d2d7bd9ad9d9a72ce156d8c25f5700c134bdff005c8e28c0f0e9512895"
# Disable platform warning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecurePlatformWarning)

class VT_Download(object):
    """
    VT_Download class, query virustotal, download sample
    """

    def download(self, sample_sha1):
        """
        query virustotal, get sample from virustotal based on sample sha1
        """
        downloaded_file = None
        try:
            params = {'apikey': VTKey, 'hash': sample_sha1}
            response = requests.get('https://www.virustotal.com/vtapi/v2/file/download', params=params)
            downloaded_file = response.content
        except Exception, e:
            #print e
            pass
        finally:
            #print downloaded_file
            if not downloaded_file:
                downloaded_file = None
            elif downloaded_file.rfind(r'<Error><Code>NoSuchKey</Code><Message>The specified key does not exist.</Message></Error>') != -1:
                downloaded_file = None
            else:
                pass
            return downloaded_file

if __name__ == '__main__':
    vt_query = VT_Download()
    sha1 = '5de8df297641eb2d24e78c5c589ea2b8f3416d0d'
    content = vt_query.download(sha1)
    download_dir = sys.argv[1]
    file_path = os.path.join(download_dir, sha1)
    with open(file_path, 'wb') as f:
        f.write(content)
    print content