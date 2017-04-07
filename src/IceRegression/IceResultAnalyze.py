import os
import zipfile
import sys
import json
import re
import shutil

def is_zip(file):
    result = False
    if os.path.exists(file) and os.path.splitext(file) == 'zip':
        result = True
    return result

def unzip_result(zip_folder, out_folder=""):
    is_dir = False
    is_zip_file = False
    if os.path.isdir(zip_folder):
        is_dir = True
    if not is_dir and is_zip(zip_folder):
        is_zip_file = True
    if not is_dir and not is_zip_file:
        return out_folder
    if len(out_folder) != 0 and not os.path.exists(out_folder):
        os.mkdir(out_folder)
    if len(out_folder) == 0:
        if is_dir:
            out_folder = zip_folder
        else:
            out_folder = os.path.dirname(zip_folder)
    if is_dir:
        for root, dirs, files in os.walk(zip_folder):
            for name in files:
                if name.split('.')[-1] == 'zip':
                    path = os.path.join(root, name)
                    try:
                        zipf = zipfile.ZipFile(path)
                        for name in zipf.namelist():
                            if 'ice.cfg' in name:
                                print name
                                zipf.extract(name, path=out_folder,pwd='virus')
                        #zipf.extractall(path=out_folder, members=['ivrV2.log', 'api.log'], pwd='virus')
                    except Exception, data:
                        print name
                        print Exception, ":", data
                    finally:
                        zipf.close()
    else:
        zipf = zipfile.ZipFile(zip_folder)
        try:
            zipf.extractall(path=out_folder, pwd='virus')
        except Exception, data:
            print zip_folder
            print Exception, ":", data
            raise AssertionError("unzip %s error." % out_folder)
        finally:
            zipf.close()
    return out_folder


def analyze_flirt(result_folder):
    for root, dirs, files in os.walk(result_folder):
        for file in files:
            if file == 'ice.cfg':
                ice_cfg_file = os.path.join(root, file)
                with open(ice_cfg_file, 'r') as f:
                    ice_cfg_data = json.load(f)
                if 'IceCheckerStructualBytes' in ice_cfg_data['Report'].keys():
                    if (len(ice_cfg_data['Report']['IceCheckerStructualBytes']) > 0):
                        return True
    return False

def analyze_stalling(result_folder):
    for root, dirs, files in os.walk(result_folder):
        for file in files:
            if file == 'ice.cfg':
                ice_cfg_file = os.path.join(root, file)
                with open(ice_cfg_file, 'r') as f:
                    ice_cfg_data = json.load(f)
                if 'IceCheckerLoop' in ice_cfg_data['Report'].keys():
                    if (len(ice_cfg_data['Report']['IceCheckerLoop']) > 0):
                        return True
    return False

def analyze_evasion(result_folder):
    d9_regex = re.compile(r"^Malicious score is(\s+)(\d+)\. Decision is (\d+).")
    for root, dirs, files in os.walk(result_folder):
        for file in files:
            if file == 'ivrV2.log':
                ivr_file = os.path.join(root, file)
                with open(ivr_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) < 7:
                        return False
                    else:
                        for line in lines:
                            match_result = d9_regex.match(line)
                            if match_result:
                                if match_result.group(3) == '9':
                                    return True
    return False

def ice_result_check(filename, result_folder):
    if 'Flirt' in filename:
        return analyze_flirt(result_folder)
    elif 'Stalling' in filename:
        return analyze_stalling(result_folder)
    elif 'Evasion' in filename:
        return analyze_evasion(result_folder)
    return False

def clean_result(Dir):
    if os.path.isdir(Dir):
        paths = os.listdir(Dir)
        for path in paths:
            filePath = os.path.join(Dir, path)
            if os.path.isfile(filePath):
                try:
                    os.remove(filePath)
                except (Exception, IOError) as e:
                    print e
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath, True)
    shutil.rmtree(Dir)
    return True


class ICE_Parser(object):
    def __init__(self):
        pass
    def __unzip_ice_cfg(self, result_folder):
        retv = False
        if not os.path.exists(result_folder):
            return retv
        self._ice_cfg_file_ = ""
        for root, dirs, files in os.walk(result_folder):
            for name in files:
                if name.split('.')[-1] == 'zip':
                    path = os.path.join(root, name)
                    try:
                        zipf = zipfile.ZipFile(path)
                        for name in zipf.namelist():
                            if 'ice.cfg' in name:
                                zipf.extract(name, path=result_folder,pwd='virus')
                                self._ice_cfg_file_ = os.path.join(result_folder, name)
                               # print "self._ice_cfg_file_ = %s" % self._ice_cfg_file_
                    except Exception, data:
                        print Exception, ":", data
                    finally:
                        zipf.close()
        if len(self._ice_cfg_file_) != 0:
            retv = True
        return retv

    def __clean_folder(self, folder):
        if os.path.isdir(folder):
            paths = os.listdir(folder)
            for path in paths:
                filePath = os.path.join(folder, path)
                if os.path.isfile(filePath):
                    try:
                        os.remove(filePath)
                    except (Exception, IOError) as e:
                        print e
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath, True)
            shutil.rmtree(folder)

    def analyze_flirt(self, result_folder):
        if not self.__unzip_ice_cfg(result_folder):
            raise AssertionError("unzip ice.cfg to %s error" % result_folder)
        ice_log_folder = os.path.join(result_folder, "ICELOG")
        with open(self._ice_cfg_file_, 'r') as f:
            ice_cfg_data = json.load(f)
        if 'IceCheckerStructualBytes' in ice_cfg_data['Report'].keys():
            if (len(ice_cfg_data['Report']['IceCheckerStructualBytes']) > 0):
                self.__clean_folder(ice_log_folder)
                return True
        self.__clean_folder(ice_log_folder)
        raise AssertionError("Flirt check fail: IceCheckerStructualBytes is empty in %s" % self._ice_cfg_file_)


    def analyze_stalling(self, result_folder):
        if not self.__unzip_ice_cfg(result_folder):
            raise AssertionError("unzip ice.cfg to %s error" % result_folder)
        ice_log_folder = os.path.join(result_folder, "ICELOG")
        with open(self._ice_cfg_file_, 'r') as f:
            ice_cfg_data = json.load(f)
        if 'IceCheckerLoop' in ice_cfg_data['Report'].keys():
            if (len(ice_cfg_data['Report']['IceCheckerLoop']) > 0):
                self.__clean_folder(ice_log_folder)
                return True
        self.__clean_folder(ice_log_folder)
        raise AssertionError("Stalling check fail: IceCheckerLoop is empty in %s" % self._ice_cfg_file_)


    def analyze_evasion(self, result_folder):
        if not os.path.exists(result_folder):
            raise AssertionError("result folder: %s not exist" % result_folder)
        d9_regex = re.compile(r"^Malicious score is(\s+)(\d+)\. Decision is (\d+).")
        ivrv2_log_file = os.path.join(result_folder, "ivrV2.log")
        if os.path.exists(ivrv2_log_file):
            with open(ivrv2_log_file, 'r') as f:
                lines = f.readlines()
                if len(lines) < 7:
                    raise AssertionError("ivrV2.log contains less than 7 lines")
                else:
                    for line in lines:
                        match_result = d9_regex.match(line)
                        if match_result:
                            if match_result.group(3) == '9':
                                return True
        raise AssertionError("Not D9, Evasion maybe not pass, please check.")

def main():
    in_folder = ""
    out_folder = ""
    if len(sys.argv) == 2:
        in_folder = sys.argv[1]
    elif len(sys.argv) == 3:
        in_folder = sys.argv[1]
        out_folder = sys.argv[2]
    else:
        print "arguments error"
        return

    result_folder = unzip_result(in_folder, out_folder)

    if analyze_flirt(result_folder):
        print "FLIRT OK"

    if analyze_evasion(result_folder):
        print "Evasion OK"

    if analyze_stalling(result_folder):
        print "Stalling OK"

    need_clean_folder = os.path.join(result_folder, "ICELOG")
    clean_result(need_clean_folder)

def main_2():

    ice_parser = ICE_Parser()
    if ice_parser.analyze_evasion(sys.argv[1]):
        print "Evasion OK"
    if ice_parser.analyze_flirt(sys.argv[1]):
        print "FLIRT OK"
    if ice_parser.analyze_stalling(sys.argv[1]):
        print "Stalling OK"


if __name__ == '__main__':
    main_2()
