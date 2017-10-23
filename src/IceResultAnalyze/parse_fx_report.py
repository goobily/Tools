import os
import sys
import json

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.cElementTree as ET

'''
report_file = r'F:\work\EvasiveSourcing\LLTrendXPatchedReport\winxp-sp3m\6236d295b73a364b060e34ed54c775ce772ddd573d5f1e51e29bc39d0319d0bf.xml'

tree = ET.ElementTree(file=report_file)

namespace = '{http://www.fireeye.com/alert/2013/AlertSchema}'

print tree.find('.//{0}original'.format(namespace)).text

result = tree.find('.//{0}alert'.format(namespace))
print result.attrib['severity']

result = tree.findall('.//malicious-alert'.format(namespace))
for item in result:
    print item.attrib['classtype'], item.find('display-msg').text


detection = ['majr', 'minr', 'crit']
'''

def extract_detection_info(fx_report_file):
    detection_info = {}
    if not os.path.exists(fx_report_file) or not fx_report_file.endswith('xml'):
        return detection_info
    xml_tree = ET.ElementTree(file=fx_report_file)
    namespace = '{http://www.fireeye.com/alert/2013/AlertSchema}'
    file_name = xml_tree.find('.//{0}original'.format(namespace)).text
    detection_result = xml_tree.find('.//{0}alert'.format(namespace)).attrib['severity']
    detection_behavior = []
    ele_behaviors = xml_tree.findall('.//malicious-alert'.format(namespace))
    for ele in ele_behaviors:
        detection_behavior.append('{0}: {1}'.format(ele.attrib['classtype'], ele.find('display-msg').text))
    detection_info = {
        'name': file_name,
        'detection': detection_result,
        'behavior': detection_behavior
    }

    return detection_info

def parse_all(in_fx_report_dir, out_detection_result_file):

    if not os.path.exists(in_fx_report_dir):
        print "{0} NOT EXIST!".format(in_fx_report_dir)
        return False
    detected_samples = []
    for root, dirs, files in os.walk(in_fx_report_dir):
        for file in files:
            file_info = extract_detection_info(os.path.join(root, file))
            if file_info['detection'] == 'majr' or file_info['detection'] == 'crit':
                detected_samples.append(file_info)
            else:
                print '{0} Not detected'.format(file)
    if len(detected_samples) != 0:
        with open(out_detection_result_file, 'w') as f:
            detection_data = {
                'detected_count': len(detected_samples),
                'detected_samples': detected_samples
            }
            json.dump(detection_data, f, indent=2)
    return True

def main():
    parse_all(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
