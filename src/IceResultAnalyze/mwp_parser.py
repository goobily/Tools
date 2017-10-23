import json
import sys
import os
def extract_tc_indicator(report_path):
    all_result = {}
    classcificer = {}
    with open(report_path, 'r') as fd:
        for line in fd.readlines():
            r = json.loads(line)
            entries = r['rl']['entries']
            for entry in entries:
                sha1 = entry['query_hash']['sha1']
                status = entry['status']
                try:
                    sha1 = entry['query_hash']['sha1']
                    first_seen = entry['first_seen']
                    status = entry['status']
                    family_name = entry['classification']['family_name']
                    all_result[sha1] = (status, first_seen)
                    family_sample_info = '%s,%s,%s' % (sha1, status, first_seen)
                    #print family_sample_info
                    if not family_name in classcificer.keys():
                        classcificer[family_name] = [family_sample_info]
                    else:
                        classcificer[family_name].append(family_sample_info)
                    #print '################################################'
                   # print('%s,%s,%s,%s'%(sha1, status, family_name, first_seen))
                except Exception as e:
                    if not status in classcificer.keys():
                        classcificer[status] = [sha1]
                    else:
                        classcificer[status].append(sha1)
                    print(entry)
    print "Family Num: %d" % len(classcificer)
    return classcificer

def main():
    if len(sys.argv) != 3:
        print "Usage: %s in_rlReportFile out_FamilyClassificationFile" % os.path.basename(__file__)
        return
    result_classcificer = extract_tc_indicator(sys.argv[1])
    with open(sys.argv[2], 'w') as f:
        json.dump(result_classcificer, f, indent=2)

if __name__ == '__main__':
    main()