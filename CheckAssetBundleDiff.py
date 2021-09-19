import os
import hashlib
import csv

md5 = hashlib.md5
work_space_path = '/Volumes/Work/program/client'


def md5_check_result(file_name):
    f = open(file_name, 'rb')
    content = f.read()
    f.close()
    m = md5(content)
    f_md5 = m.hexdigest()
    return f_md5


def get_manifest_assets_file(ast_file):
    f = open(ast_file, 'r')
    line = f.readline()
    start_assets = False
    file_list = []
    while line:
        if line.startswith('Assets:'):
            start_assets = True
        if start_assets and line.startswith('-'):
            file_path = line.lstrip('- ').rstrip()
            file_list.append(file_path)
        line = f.readline()
    f.close()
    return file_list


md5_file_list = []


def start_check(ast_bundle_path):
    assets_files = get_manifest_assets_file(ast_bundle_path)
    for k in assets_files:
        file = os.path.join(work_space_path, k)
        if os.path.exists(file):
            file_list = [ast_bundle_path, file]
            pre_md5 = md5_check_result(file)
            file_list.append(pre_md5)
            md5_file_list.append(file_list)
    return md5_file_list


def get_asset_bundle_manifest():
    asset_bundle_path = work_space_path + '/AssetBundles/Android'
    files = os.walk(asset_bundle_path)
    for path, dir_list, file_list in files:
        for file_name in file_list:
            if file_name.endswith('manifest'):
                file_path = os.path.join(path, file_name)
                if os.path.exists(file_path):
                    start_check(file_path)


asset_csv_file = 'assetBundle.csv'


def write_file_csv(csv_file, content):
    with open(csv_file, 'w') as f:
        write = csv.writer(f)
        write.writerows(content)


def write_asset_bundle_csv():
    get_asset_bundle_manifest()
    write_file_csv(asset_csv_file, md5_file_list)


def get_asset_dependencies_md5_list(csv_file, ast_bundle_name):
    child_path = []
    with open(csv_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, rows in enumerate(reader):
            asset_bundle_name = rows[0]
            if asset_bundle_name.endswith(ast_bundle_name):
                csv_list = [rows[1], rows[2]]
                child_path.append(csv_list)
    return child_path


def diff_patch_csv_file(patch_last, patch_cur):
    if os.path.exists(patch_last) and os.path.exists(patch_cur):
        csv_fileA = open(patch_last, 'r')
        reader_last = list(csv.reader(csv_fileA))
        csv_fileB = open(patch_cur, 'r')
        reader_cur = list(csv.reader(csv_fileB))
        diff_list = []
        for i, rows in enumerate(reader_last):
            file_name = rows[0]
            file_md5 = rows[1]
            for k, cur_rows in enumerate(reader_cur):
                if file_name == cur_rows[0]:
                    if file_md5 != cur_rows[1]:
                        diff_item = [file_name, file_md5, cur_rows[1]]
                        diff_list.append(diff_item)
        csv_fileB.close()
        csv_fileA.close()
        return diff_list


if __name__ == '__main__':
    # test_key = 'renderresources_assetbundle.manifest'
    # child = get_asset_dependencies_md5_list(asset_csv_file, test_key)
    # write_file_csv('patchA.csv', child)
    diff = diff_patch_csv_file('patchA.csv', 'patchB.csv')
    write_file_csv('patch.csv', diff)

