#!/usr/bin/python3
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json
import atheris
import tabulate

def ConsumeRandomListofNumLists(fdp):
    fuzzed_list = []
    max_range = fdp.ConsumeInt(1000)
    num_of_int = fdp.ConsumeInt(1000)
    for _ in range(max_range):
        fuzzed_list.append(fdp.ConsumeIntListInRange(num_of_int, 1, 1000))
    return fuzzed_list

def ConsumeRandomListofStringLists(fdp):
    fuzzed_list = []
    max_range = fdp.ConsumeInt(1000)
    for _ in range(max_range):
        str_list = list(ConsumeUnicodeNoSurrogates(100))
        fuzzed_list.append(str_list)
    return fuzzed_list

def ConsumeRandomListofStrings(fdp):
    fuzzed_list = []
    max_range = fdp.ConsumeInt(1000)
    for _ in range(max_range):
        fuzzed_list.append(ConsumeUnicodeNoSurrogates(100))
    return fuzzed_list


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    tabulate_formats = list(tabulate._table_formats.keys())
    table_format = fdp.PickValueInList(tabulate_formats)
    # table_format = tabulate_formats[fdp.ConsumeIntInRange(0, len(tabulate_formats)-1)]

    try:
        chunks = tabulate._CustomTextWrap()._wrap_chunks(chunks=fdp.ConsumeUnicodeNoSurrogates(100))
    except AttributeError:
        pass

    # Create random dictionary
    try:
        fuzzed_dict = json.loads(fdp.ConsumeString(sys.maxsize))
    except:
        return
    if type(fuzzed_dict) is not dict:
        return


    t1 = tabulate.tabulate(
        fuzzed_dict,
        tablefmt=table_format
    )

    t4 = tabulate.tabulate(ConsumeRandomListofStrings(fdp), tablefmt=table_format)

    t3 = tabulate.tabulate(ConsumeRandomListofStringLists(fdp), tablefmt=table_format)

    t2 = tabulate.tabulate(ConsumeRandomListofNumLists(fdp), tablefmt=table_format)
    

    
def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
