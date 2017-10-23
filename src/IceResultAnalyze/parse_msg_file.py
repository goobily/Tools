import win32com.client
import os
import sys
import xlrd
import argparse

'''
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg = outlook.OpenSharedItem(r"F:\work\EvasiveSourcing\RansomwareBanchmarkMail\ddan-2017-07-03.msg")

print msg.SenderName
print msg.SenderEmailAddress
print msg.SentOn
print msg.To
print msg.CC
print msg.BCC
print msg.Subject
print msg.Body

count_attachments = msg.Attachments.Count
if count_attachments > 0:
    for item in range(count_attachments):
        print msg.Attachments.Item(item + 1).Filename
        msg.Attachments.Item(item + 1).SaveAsFile(os.path.join(r"F:\work\EvasiveSourcing\RansomwareBanchmarkExcel", msg.Attachments.Item(item + 1).Filename))


del outlook, msg
'''


def extract_excel_from_msg(in_msg_dir, out_excel_dir):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    for root, dirs, files in os.walk(in_msg_dir):
        for file in files:
            if file.endswith(".msg"):
                msg = outlook.OpenSharedItem(os.path.join(root, file))
                print msg.SenderName
                print msg.SenderEmailAddress
                print msg.SentOn
                print msg.To
                print msg.CC
                print msg.BCC
                print msg.Subject
                print msg.Body
                att = msg.Attachments
                for i in att:
                    i.SaveAsFile(os.path.join(out_excel_dir, i.FileName))  # Saves the file with the attachment name
                del msg
    del outlook


def parse_excel_file(excel_file, sheet_name, out_sha1_file):
    try:
        workbook = xlrd.open_workbook(excel_file)
        sheet_rawdata_exec = workbook.sheet_by_name(sheet_name)
        sha1_list = []
        sha256_list = []
        for rownum in range(sheet_rawdata_exec.nrows):
            if rownum == 0:
                continue
            sha1 = sheet_rawdata_exec.cell(rownum, 1).value
            sha256 = sheet_rawdata_exec.cell(rownum, 2).value
            print sha1, sha256
            sha1_list.append(sha1)
            sha256_list.append(sha256)
        with open(out_sha1_file, 'a') as f:
            for item in sha1_list:
                f.write(str(item))
                f.write('\n')
    except Exception, e:
        print str(e)

def parse_excel_dir(in_excel_dir, sheet_name, out_sha1_file):
    if not os.path.exists(in_excel_dir):
        print "%s NOT EXIST" % (in_excel_dir)
        return
    for root, dirs, files in os.walk(in_excel_dir):
        for file in files:
            parse_excel_file(os.path.join(root, file), sheet_name, out_sha1_file)

def parse_msg(in_msg_dir, out_excel_dir):
    if not os.path.exists(in_msg_dir):
        return
    if not os.path.exists(out_excel_dir):
        os.mkdir(out_excel_dir)
    extract_excel_from_msg(in_msg_dir, out_excel_dir)

def parse_excel(in_excel_dir, sheet_name, out_sha1_file):
    parse_excel_dir(in_excel_dir, sheet_name, out_sha1_file)


usage_callback = {
    'msg': parse_msg,
    'excel': parse_excel
}

valid_sheet_name = [
    'rawdata_exec',
    'rawdata_All'
]

def main():
    parser = argparse.ArgumentParser(description='parse ddan ransom msg file with attachment')

    parser.add_argument(
        '--usage-type',
        required=True,
        type=str,
        choices=usage_callback.keys(),
        help='choose usage type for this python script'
    )

    parser.add_argument(
        '--input-folder',
        required=True,
        help='the input folder of msg files or excel files'
    )

    parser.add_argument(
        '--output-excel-folder',
        default=os.path.join(os.path.abspath(os.curdir), 'extracted_excel'),
        help='the output folder to store extracted excel from msg'
    )

    parser.add_argument(
        '--sheet-name',
        type=str,
        choices=valid_sheet_name,
        default='rawdata_exec',
        help='choose the sheet need to parse'
    )

    parser.add_argument(
        '--output-sha1-file',
        default=os.path.join(os.path.abspath(os.curdir), 'rawdata_sha1.txt'),
        help='the output file to store the extracted sha1'
    )

    args = vars(parser.parse_args())

    usage_type = args['usage_type']
    input_folder = args['input_folder']
    output_excel_folder = args['output_excel_folder']
    sheet_name = args['sheet_name']
    output_sha1_file = args['output_sha1_file']

    print usage_type
    print input_folder
    print output_excel_folder
    print sheet_name
    print output_sha1_file

    if usage_type == 'msg':
        parse_msg(input_folder, output_excel_folder)
    elif usage_type == 'excel':
        parse_excel(input_folder, sheet_name, output_sha1_file)


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)