import json
import sys
import os

def analyze_ll_report(report):
    if not os.path.isfile(report):
        print 'Input file:[%s] does not exist!' % report
        return None
    with open(report, 'r') as f:
        report_dict = json.load(f) # dict
    score = 0
    if 'score' in report_dict['data'].keys():
        score = report_dict['data']['score']
    evasion_rules = []
    malicious_activity = []
    if 'malicious_activity' in report_dict['data'].keys():
        malicious_activity = report_dict['data']['malicious_activity']
        for rule in malicious_activity:
            if 'Evasion' in rule:
                evasion_rules.append(rule)

    result = {
        'score': score,
        'sample_info': {
            'md5': report_dict['data']['analysis_subject']['md5'],
            'sha1': report_dict['data']['analysis_subject']['sha1'],
            'sha256': report_dict['data']['analysis_subject']['sha256']
        },
        'malicious_activity': malicious_activity
    }
    return len(evasion_rules), result

def extract(src_report_dir, dest_result_dir):
    if not os.path.exists(src_report_dir):
        print 'Input path:[%s] does not exist!' % src_report_dir
        return
    if not os.path.exists(dest_result_dir):
        os.mkdir(dest_result_dir)
    result_file = os.path.join(dest_result_dir, 'result.json')
    print result_file
    result_data = []
    malicious_num = 0
    malicious_samples = []
    if os.path.isfile(src_report_dir):
        evasion_rule_count, info = analyze_ll_report(src_report_dir)
        if evasion_rule_count > 0:
            result_data.append(info)
        if info['score'] >= 70:
            malicious_num += 1
            malicious_samples.append(info)
    elif os.path.isdir(src_report_dir):
        for root, dirs, files in os.walk(src_report_dir):
            for file in files:
                report_file_path = os.path.join(root, file)
                evasion_rule_count, info = analyze_ll_report(report_file_path)
                if evasion_rule_count > 0:
                    result_data.append(info)
                if info['score'] >= 70:
                    malicious_num += 1
                    malicious_samples.append(info)

    report = {
        'total_malicious': malicious_num,
        'malicious_samples': malicious_samples,
        'total_evasion': len(result_data),
        'evasion_samples': result_data
    }
    with open(result_file, 'w') as f:
        json.dump(report, f, indent=2)

def print_usage():
    print '%s [in]report_path [out]result_path' % os.path.basename(__file__)

def main():
    if len(sys.argv) != 3:
        print_usage()
        return
    extract(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
