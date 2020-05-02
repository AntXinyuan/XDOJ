import hashlib
import json
import os
import zipfile

from XDOJ import settings
from utils.tools import rand_str, natural_sort_key


class ZipException(Exception):
    def __init__(self, msg):
        self.msg = msg


def process_zip(uploaded_zip_file, spj=None, dir=''):
    """
    解压缩测试点压缩包，按照特定格式存储在系统指定位置，并返回相应信息
    """
    try:
        zip_file = zipfile.ZipFile(uploaded_zip_file, "r")
    except zipfile.BadZipFile:
        raise ZipException("文件不是有效的压缩包！")
    name_list = zip_file.namelist()
    test_case_list = filter_name_list(name_list, spj=spj, dir=dir)
    if not test_case_list:
        raise ZipException("压缩包中不包含任何有效的测试点文件对！")
    test_case_id = rand_str()
    test_case_dir = os.path.join(settings.TEST_CASE_ROOT, test_case_id).replace('\\', '/')
    os.mkdir(test_case_dir)
    os.chmod(test_case_dir, 0o710)

    size_cache = {}
    md5_cache = {}

    for item in test_case_list:
        with open(os.path.join(test_case_dir, item), "wb") as f:
            content = zip_file.read(f"{dir}{item}").replace(b"\r\n", b"\n")
            size_cache[item] = len(content)
            if item.endswith(".out"):
                md5_cache[item] = hashlib.md5(content.rstrip()).hexdigest()
            f.write(content)
    test_case_info = {"spj": spj, "test_cases": {}}

    info = []

    if spj:
        for index, item in enumerate(test_case_list):
            data = {"input_name": item, "input_size": size_cache[item]}
            info.append(data)
            test_case_info["test_cases"][str(index + 1)] = data
    else:
        # ["1.in", "1.out", "2.in", "2.out"] => [("1.in", "1.out"), ("2.in", "2.out")]
        test_case_list = zip(*[test_case_list[i::2] for i in range(2)])
        for index, item in enumerate(test_case_list):
            data = {"stripped_output_md5": md5_cache[item[1]],
                    "input_size": size_cache[item[0]],
                    "output_size": size_cache[item[1]],
                    "input_name": item[0],
                    "output_name": item[1]}
            info.append(data)
            test_case_info["test_cases"][str(index + 1)] = data

    with open(os.path.join(test_case_dir, "info"), "w", encoding="utf-8") as f:
        f.write(json.dumps(test_case_info, indent=4))

    for item in os.listdir(test_case_dir):
        os.chmod(os.path.join(test_case_dir, item), 0o640)

    return info, test_case_id


def filter_name_list(name_list, spj, dir=''):
    """
        识别并过滤有效的测试点文件
        测试点文件命名格式：1.in   1.out
    """
    ret = []
    prefix = 1
    if spj:
        while True:
            in_name = f"{prefix}.in"
            if f"{dir}{in_name}" in name_list:
                ret.append(in_name)
                prefix += 1
                continue
            else:
                return sorted(ret, key=natural_sort_key)
    else:
        while True:
            in_name = f"{prefix}.in"
            out_name = f"{prefix}.out"
            if f"{dir}{in_name}" in name_list and f"{dir}{out_name}" in name_list:
                ret.append(in_name)
                ret.append(out_name)
                prefix += 1
                continue
            else:
                return sorted(ret, key=natural_sort_key)
