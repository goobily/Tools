# coding: utf-8

import logging
import os
import sys

import DirectoryShallowWalker


class SCReportWalker(DirectoryShallowWalker.DirectoryShallowWalker):
    def __init__(self):
        self._count = 0

    def process_directory(self, dir_path):
        logging.info("Processing directory: %s", dir_path)

        all_dir = os.path.join(dir_path, "All")
        for f in os.listdir(all_dir):
            single_sample_dir = os.path.join(all_dir, f)
            if os.path.isdir(single_sample_dir):
                # Processing report.txt
                for g in os.listdir(single_sample_dir):
                    report_file = os.path.join(single_sample_dir, g)
                    if report_file.lower().endswith("report.txt") and os.path.isfile(report_file):
                        try:
                            self.process_one_file(report_file)
                        except:
                            logging.exception("Error in processing %s", report_file)

    def is_directory_interesting(self, dir_path):
        all_dir = os.path.join(dir_path, "All")
        return os.path.exists(all_dir) and os.path.isdir(all_dir)

    def process_one_file(self, src):
        sha1 = None
        detection = False
        with open(src, "r") as f:
            for l in f:
                line = l.strip().lower()
                if line.startswith("sha1:"):
                    sha1 = line[5:].strip()
                elif line.startswith("result:"):
                    detection = line[7:].strip() == "9"

        if detection and sha1:
            print sha1

        self._count += 1

    def get_count(self):
        return self._count


def main():
    walker = SCReportWalker()
    for src_dir in sys.argv[1:]:
        walker.walk(src_dir)

    logging.info("Total: %d file(s) processed.", walker.get_count())


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(levelname)s <%(process)d:%(thread)d> %(message)s", level=logging.INFO)
    main()
