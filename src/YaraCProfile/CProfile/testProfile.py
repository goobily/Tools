# coding: utf-8

import StringIO
import logging
import os
import re
import yara

YARA_RULE = """
rule CommonProlog
{
    strings:
        $prolog_string = { 55 8B EC ?? ?? ?? ?? 05 }

    condition:
        $prolog_string

}
"""

YARA_RULE_MULTIPLE = """
rule CommonProlog
{
    strings:
        $prolog_string = { 55 8B EC ?? ?? ?? ?? 05 }

    condition:
        $prolog_string
}

rule CommonProlog2
{
    strings:
        $prolog_string = { 55 8B EC ?? ?? ?? ?? 00 }

    condition:
        $prolog_string
}

rule WildcardExample
{
    strings:
       $hex_string = { E2 34 ?? C8 A? FB }

    condition:
       $hex_string
}
"""


def test_regex(regex_pattern, data):
    # type: (re.__Regex, str) -> int
    count = 0
    for e in regex_pattern.finditer(data):
        count += 1

    return count


def test_regex_multiple(regex_pattern_list, data):
    # type: (list, str) -> int
    count = 0
    for regex_pattern in regex_pattern_list:
        count += test_regex(regex_pattern, data)

    return count


def test_yara(yara_pattern, data):
    match_result = yara_pattern.match(data=data)
    return len(match_result[0].strings) if match_result else 0


LOOP_TIME = 1000


def test_regex_many_times(regex_pattern_list, data):
    i = 0
    while i < LOOP_TIME:
        test_regex_multiple(regex_pattern_list, data)
        i += 1


def test_yara_many_times(yara_pattern_multiple, data):
    i = 0
    while i < LOOP_TIME:
        test_yara(yara_pattern_multiple, data)
        i += 1


def main():
    regex_pattern = re.compile(r"\x55\x8B\xEC.{4}\x05")
    yara_pattern = yara.compile(source=YARA_RULE)

    data_io = StringIO.StringIO()
    data_io.write(os.urandom(1024 * 1024 * 64))
    data = data_io.getvalue()

    import cProfile
    print "单条rule："
    cProfile.runctx("test_regex(regex_pattern, data)", globals(), locals())
    cProfile.runctx("test_yara(yara_pattern, data)", globals(), locals())

    print "3条rule："

    regex_pattern_multiple = [re.compile(r"\x55\x8B\xEC.{4}\x05"), re.compile(r"\x55\x8B\xEC.{4}\x00"),
                              re.compile(r"\x55\x8B\xEC.{4}\x01")]
    cProfile.runctx("test_regex_multiple(regex_pattern_multiple, data)", globals(), locals())

    yara_pattern_multiple = yara.compile(source=YARA_RULE_MULTIPLE)
    cProfile.runctx("test_yara(yara_pattern_multiple, data)", globals(), locals())

    print "单条rule 1000次："

    data_io = StringIO.StringIO()
    data_io.write(os.urandom(1024 * 64))
    data = data_io.getvalue()

    cProfile.runctx("test_regex_many_times([regex_pattern], data)", globals(), locals())
    cProfile.runctx("test_yara_many_times(yara_pattern, data)", globals(), locals())

    print "3条rule 1000次："

    cProfile.runctx("test_regex_many_times(regex_pattern_multiple, data)", globals(), locals())
    cProfile.runctx("test_yara_many_times(yara_pattern_multiple, data)", globals(), locals())


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s <%(process)d:%(thread)d> %(message)s", level=logging.DEBUG)

    try:
        main()
    except Exception:
        logging.exception("Error in main.")