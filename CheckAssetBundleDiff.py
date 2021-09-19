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


def get_asset_bundle_manifest():
    asset_bundle_path = work_space_path + '/AssetBundles/Android'
    files = os.walk(asset_bundle_path)
    for path, dir_list, file_list in files:
        for file_name in file_list:
            if file_name.endswith('manifest'):
                file_path = os.path.join(path, file_name)
                if os.path.exists(file_path):
                    start_check(file_path)


if __name__ == '__main__':
    get_asset_bundle_manifest()
    with open('assetBundle.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(md5_file_list)
