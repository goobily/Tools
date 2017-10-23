from __future__ import division
import sys
import argparse
import os
from ice_parser import ICE_Parser

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) >= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def get_ice_rerun_behavior_contribution(result_all_folder, rate_threshold):

    ice_parser_ins = ICE_Parser()
    num_all_ice_rerun = 0
    num_more_behavior = 0
    for root, dirs, files in os.walk(result_all_folder):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            name = ice_parser_ins.get_name(dir_path)
            if name is not None and ice_parser_ins.api_log_should_contain(dir_path, "RERUN BY ICE"):
                num_all_ice_rerun += 1
                num_before_ice_rerun, num_after_ice_rerun = ice_parser_ins.get_api_count_split_by_specific_log(dir_path, "RERUN BY ICE ")
                num_before_ice_rerun -= 41
                num_after_ice_rerun -= 2
                if num_before_ice_rerun >0 and num_after_ice_rerun > 0:
                    actual_rate = float("%0.2f" % (num_after_ice_rerun/num_before_ice_rerun))
                    if actual_rate > rate_threshold:
                        num_more_behavior += 1
                        print "[%d/%d]  %s" % (num_before_ice_rerun, num_after_ice_rerun, name)

    print "more behavior: [%d/%d]" % (num_more_behavior, num_all_ice_rerun)

def get_ice_patched_info(result_all_folder):

    ice_parser_ins = ICE_Parser()
    num_all = 0
    num_patched_success = 0
    num_patched_fail = 0

    name_ice_patched_success = []
    name_ice_patched_fail = []


    for root, dirs, files in os.walk(result_all_folder):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            name = ice_parser_ins.get_name(dir_path)
            num_all += 1
            if name is not None:
                if ice_parser_ins.api_log_should_contain(dir_path, "patch[\s\S]{0,12}OK[\s\S]{0,16}patched."):
                    num_patched_success += 1
                    print "patch success: [%s]" % name
                    name_ice_patched_success.append(name)
                elif ice_parser_ins.api_log_should_contain(dir_path, "Patch[\s\S]{0,12}failed. Error:"):
                    num_patched_fail += 1
                    print "patch fail: [%s]" % name
                    name_ice_patched_fail.append(name)

    print "\ntotal: [%d]" % num_all
    print "num_patch_success: [%d/%d]" % (num_patched_success, num_all)
    print "num_patch_fail: [%d/%d]" % (num_patched_fail, num_all)

def get_prefilter_info(result_all_folder):

    ice_parser_ins = ICE_Parser()
    num_all = 0
    num_pass_prefilter = 0
    num_pass_prefilter_malicious = 0
    num_pass_sps_prefilter = 0
    num_pass_sps_prefilter_malicious = 0

    name_pass_prefilter = []
    name_new_malicious = []
    name_pass_sps_prefilter = []
    name_sps_new_malicious = []

    for root, dirs, files in os.walk(result_all_folder):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            num_all += 1
            name = ice_parser_ins.get_name(dir_path)

            if name is not None and ice_parser_ins.behaviordumper_log_should_contain(dir_path, "Start ICE with dynamic mode!"):
                num_pass_prefilter += 1
                print "pass prefilter: [%s]" % name
                name_pass_prefilter.append(name)

                decision = ice_parser_ins.decsion_should_be_malicious(dir_path)
                if decision:
                    num_pass_prefilter_malicious += 1
                    print "new malicious: [%s]" % name
                    name_new_malicious.append(name)

                if ice_parser_ins.behaviordumper_log_should_contain(dir_path, "ICE will dynamically run due to stat/ML model hit."):
                    num_pass_sps_prefilter += 1
                    print "pass sps prefilter: [%s]" % name
                    name_pass_sps_prefilter.append(name)

                    if decision:
                        num_pass_sps_prefilter_malicious +=1
                        print "sps new malicious: [%s]" % name
                        name_sps_new_malicious.append(name)

    print "\ntotal: [%d]" % num_all
    print "num_pass_prefilter: [%d/%d]" % (num_pass_prefilter, num_all)
    print "num_pass_prefilter_malicious: [%d/%d]" % (num_pass_prefilter_malicious, num_all)
    print "\nnum_pass_sps_prefilter: [%d/%d]" % (num_pass_sps_prefilter, num_all)
    print "num_pass_sps_prefilter_malicious: [%d/%d]" % (num_pass_sps_prefilter_malicious, num_all)

data_info_callback = {
    'patch': get_ice_patched_info,
    'prefilter': get_prefilter_info,
    'contribution': get_ice_rerun_behavior_contribution
}

def main():

    parser = argparse.ArgumentParser(description="Ice Result Analysis")

    parser.add_argument(
        '--result-folder',
        required=True,
        help='all result folder'
    )

    parser.add_argument(
        '--data-info',
        type=str,
        default='patch',
        choices=data_info_callback.keys(),
        required=True,
        help='choose what data info need to analysis, default is patch'
    )

    parser.add_argument(
        '--contribution-rate',
        type=float,
        default=0.20,
        help='ice contribution rate threshold'
    )

    args = vars(parser.parse_args())

    result_all_folder = args['result_folder']
    data_info_need = args['data_info']
    rate_threshold = args['contribution_rate']

    if data_info_need == 'contribution':
        data_info_callback.get(data_info_need)(result_all_folder, rate_threshold)
    else:
        data_info_callback.get(data_info_need)(result_all_folder)

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)
