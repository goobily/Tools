import os
import zipfile
import json
import re
import shutil


ICE_DYNAMIC_CHECKERS = ["IceCheckerLoop", "IceCheckerSmartRun", "IceCheckerSemanticFlow"]

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

    def __is_ice_generate_patch(self, ice_cfg_data, ice_checkers):
        if ice_cfg_data !=None and ice_cfg_data.get("Report", 0) != 0:
            for ice_checker in ice_checkers:
                if ice_checker in ice_cfg_data['Report'].keys():
                    if (len(ice_cfg_data['Report'][ice_checker]) > 0):
                        return True
        return False

    def is_ice_patched(self, result_folder):
        if not self.__unzip_ice_cfg(result_folder):
            print "unzip ice.cfg to %s error" % result_folder
            return False
        ice_log_folder = os.path.join(result_folder, "ICELOG")
        with open(self._ice_cfg_file_, 'r') as f:
            ice_cfg_data = json.load(f)
        self.__clean_folder(ice_log_folder)
        return self.__is_ice_generate_patch(ice_cfg_data, ICE_DYNAMIC_CHECKERS)

    def ice_cfg_should_contain_flirt(self, result_folder):
        if not self.__unzip_ice_cfg(result_folder):
            print "unzip ice.cfg to %s error" % result_folder
            return False
        ice_log_folder = os.path.join(result_folder, "ICELOG")
        with open(self._ice_cfg_file_, 'r') as f:
            ice_cfg_data = json.load(f)
        if 'IceCheckerStructualBytes' in ice_cfg_data['Report'].keys():
            if (len(ice_cfg_data['Report']['IceCheckerStructualBytes']) > 0):
                self.__clean_folder(ice_log_folder)
                return True
        self.__clean_folder(ice_log_folder)
        print "Flirt check fail: IceCheckerStructualBytes is empty in %s" % self._ice_cfg_file_
        return False


    def ice_cfg_should_contain_stalling(self, result_folder):
        if not self.__unzip_ice_cfg(result_folder):
            print "unzip ice.cfg to %s error" % result_folder
            return False
        ice_log_folder = os.path.join(result_folder, "ICELOG")
        with open(self._ice_cfg_file_, 'r') as f:
            ice_cfg_data = json.load(f)
        if 'IceCheckerLoop' in ice_cfg_data['Report'].keys():
            if (len(ice_cfg_data['Report']['IceCheckerLoop']) > 0):
                self.__clean_folder(ice_log_folder)
                return True
        self.__clean_folder(ice_log_folder)
        print "Stalling check fail: IceCheckerLoop is empty in %s" % self._ice_cfg_file_
        return False

    def ice_cfg_should_contain_smartrun(self, result_folder):
        if not self.__unzip_ice_cfg(result_folder):
            print "unzip ice.cfg to %s error" % result_folder
            return False
        ice_log_folder = os.path.join(result_folder, "ICELOG")
        with open(self._ice_cfg_file_, 'r') as f:
            ice_cfg_data = json.load(f)
        if 'IceCheckerSmartRun' in ice_cfg_data['Report'].keys():
            if (len(ice_cfg_data['Report']['IceCheckerSmartRun']) > 0):
                self.__clean_folder(ice_log_folder)
                return True
        self.__clean_folder(ice_log_folder)
        print "SmartRun check fail: IceCheckerSmartRun is empty in %s" % self._ice_cfg_file_
        return False

    def ice_cfg_should_contain_semanticflow(self, result_folder):
        if not self.__unzip_ice_cfg(result_folder):
            print "unzip ice.cfg to %s error" % result_folder
            return False
        ice_log_folder = os.path.join(result_folder, "ICELOG")
        with open(self._ice_cfg_file_, 'r') as f:
            ice_cfg_data = json.load(f)
        if 'IceCheckerSemanticFlow' in ice_cfg_data['Report'].keys():
            if (len(ice_cfg_data['Report']['IceCheckerSemanticFlow']) > 0):
                self.__clean_folder(ice_log_folder)
                return True
        self.__clean_folder(ice_log_folder)
        print "SemanticFlow check fail: IceCheckerSemanticFlow is empty in %s" % self._ice_cfg_file_
        return False


    def decsion_should_be_malicious(self, result_folder):
        if not os.path.exists(result_folder):
            print "result folder: %s not exist" % result_folder
            return False
        d9_regex = re.compile(r"^Malicious score is(\s+)(\d+)\. Decision is (\d+).")
        ivrv2_log_file = os.path.join(result_folder, "ivrV2.log")
        if os.path.exists(ivrv2_log_file):
            with open(ivrv2_log_file, 'r') as f:
                lines = f.readlines()
                if len(lines) < 7:
                    print "ivrV2.log contains less than 7 lines"
                else:
                    for line in lines:
                        match_result = d9_regex.match(line)
                        if match_result:
                            if match_result.group(3) == '9':
                                return True
        return False


    def behaviordumper_log_should_contain(self, result_folder, match_key):
        if not os.path.exists(result_folder):
            #print "result folder: %s not exist" % result_folder
            return False
        re_pattern = re.compile(match_key)
        behaviordumper_log_file = ""
        for root, dirs, files in os.walk(result_folder):
            for file_name in files:
                if "BehaviorDumper.log." in file_name:
                    behaviordumper_log_file = os.path.join(root, file_name)
                    break
        if len(behaviordumper_log_file) == 0:
            #print "%s does not exist." % behaviordumper_log_file
            return False

        with open(behaviordumper_log_file, 'r') as f:
            for line in f.readlines():
                match_result = re_pattern.search(line)
                if match_result != None:
                    return True
        #print "%s does not contain: %s" % (behaviordumper_log_file, match_key)
        return False

    def api_log_should_contain(self, result_folder, match_key):
        if not os.path.exists(result_folder):
            #print "result folder: %s not exist" % result_folder
            return False
        re_pattern = re.compile(match_key)
        api_log_file = ""
        for root, dirs, files in os.walk(result_folder):
            for file_name in files:
                if "api.log" in file_name:
                    api_log_file = os.path.join(root, file_name)
                    break
        if len(api_log_file) == 0:
            #print "%s does not exist." % api_log_file
            return False

        with open(api_log_file, 'r') as f:
            for line in f.readlines():
                match_result = re_pattern.search(line)
                if match_result != None:
                    return True
        #print "%s does not contain: %s" % (api_log_file, match_key)
        return False

    def get_sha1(self, result_folder):
        sha1 = None
        if not os.path.exists(result_folder):
            return sha1
        for item in os.listdir(result_folder):
            report_file = os.path.join(result_folder, item)
            if report_file.lower().endswith("report.txt") and os.path.isfile(report_file):
                with open(report_file, "r") as f:
                    for l in f:
                        line = l.strip().lower()
                        if line.startswith("sha1:"):
                            sha1 = line[5:].strip()
                            return sha1
        return sha1

    def get_name(self, result_folder):
        name = None
        if not os.path.exists(result_folder):
            return name
        for item in os.listdir(result_folder):
            report_file = os.path.join(result_folder, item)
            if report_file.lower().endswith("report.txt") and os.path.isfile(report_file):
                with open(report_file, 'r') as f:
                    for l in f:
                        line = l.strip().lower()
                        if line.startswith("name:"):
                            name = line[5:].strip()
                            return name
        return name

    def get_api_count_split_by_specific_log(self, result_folder, match_key):
        num_before = 0
        num_after = 0
        if not os.path.exists(result_folder):
            return (num_before, num_after)
        api_log_file = ""
        for root, dirs, files in os.walk(result_folder):
            for file_name in files:
                if "api.log" in file_name:
                    api_log_file = os.path.join(root, file_name)
                    break
        if len(api_log_file) == 0:
            # print "%s does not exist." % api_log_file
            return (num_before, num_after)

        re_pattern = re.compile(match_key)
        with open(api_log_file, 'r') as f:
            need_search = True
            for line in f.readlines():
                if need_search and re_pattern.search(line) != None:
                    need_search = False
                if need_search:
                    num_before += 1
                else:
                    num_after += 1

        return (num_before, num_after)
