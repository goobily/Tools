# coding: utf-8
import re


class SCIvrLogFormatError(Exception):
    pass


class SCIvrLogParser(object):
    def __init__(self, fn_fd):
        self._data = {}

        if isinstance(fn_fd, str):
            with open(fn_fd, "r") as fd:
                self._parse_file(fd)
        else:
            self._parse_file(fn_fd)

    def _parse_file(self, fd):
        # 0 - initial, 1 - decision, 2 - score, 3 - static info, 4 - rule
        state = [0]
        state_machine = (
            self._parse_initial,
            self._parse_decision,
            self._parse_score,
            self._parse_static_info,
            self._parse_rule
        )
        for l in fd:
            line = l.strip()
            state_machine[state[0]](line, state)

        if state[0] != 4:
            raise SCIvrLogFormatError("IVR log is not complete. Parsing stops at state " + str(state[0]))

    def _parse_initial(self, line, state):
        if line.lower().startswith("initial virus report"):
            state[0] = 1

    def _parse_decision(self, line, state):
        self._data["decision"] = line
        state[0] = 2

    def _parse_score(self, line, state):
        m = re.match(r"Malicious score is (\d+). Decision is (\d+)\.", line)
        if m:
            self._data["score"] = m.group(1)
            state[0] = 3

    def _parse_static_info(self, line, state):
        if "static_info" in self._data:
            # %WorkingDir%\1cd240fe3fa890ec3f07f177ecdbba5306975950.exe,VSDT_EXE_ASPACK2,a49a7378,7f961b8ae286c28e7393190404f789d9,1CD240FE3FA890EC3F07F177ECDBBA5306975950
            info_list = [e.strip() for e in line.split(",")]

            if len(info_list) < 5:
                raise SCIvrLogFormatError("Error when parsing static info. Info item less than 5.")

            # file name
            file_name = info_list[0]
            if file_name.startswith("%WorkingDir%\\"):
                file_name = file_name[len("%WorkingDir%\\"):]

            self._data["static_info"]["file_name"] = file_name

            # file type
            file_type = info_list[1]
            self._data["static_info"]["file_type"] = file_type

            # md5
            md5 = info_list[3].lower()
            self._data["static_info"]["md5"] = md5

            # sha1
            sha1 = info_list[4].lower()
            self._data["static_info"]["sha1"] = sha1

            state[0] = 4
        else:
            header = SCIvrLogParser._match_header(line)
            if header and header == "Static Information":
                self._data["static_info"] = {}

    RULE_RE_PART = re.compile(r"\[([\dA-Za-z]+)\]\s+(?:\[Score: \d+\]\s+)?\d+")

    def _parse_rule(self, line, state):
        if "rule_set" not in self._data:
            self._data["rule_set"] = set()

        m = SCIvrLogParser.RULE_RE_PART.search(line)
        if m:
            self._data["rule_set"].add(m.group(1))

    HEADER_RE = re.compile(r"\[-+\s+(.*)\s+-+\]")

    @staticmethod
    def _match_header(line):
        m = SCIvrLogParser.HEADER_RE.match(line)
        if m:
            return m.group(1)
        else:
            return ""

    def get_result(self):
        return self._data

def main():
    import sys
    ivr_file = sys.argv[1]
    p = SCIvrLogParser(ivr_file)

    rules = p.get_result()['rule_set'] # type: set

    for ruleid in rules:
        print ruleid


if __name__ == '__main__':
    main()