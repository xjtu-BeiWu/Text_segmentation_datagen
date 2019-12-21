import itertools

import os
import random
import shutil


# def split_lines(file_path):
#     result = open(file_path).read()
#     result = re.sub("[+.!_,$%^*( \"\')]+|[+——()?【】“”！。？~@#￥%……&*（）]+", ' ', result)
#     result = result.split(' ')
#     del result[-1]
#     return result


def copy_file(file_dir, tar_dir, num):
    path_dir = os.listdir(file_dir)
    sample = random.sample(path_dir, num)

    for name in sample:
        shutil.copyfile(file_dir + name, tar_dir + name)


def reorganize(file_dir, tar_dir, name_list, num):
    # if not os.path.exists(tar_dir):
    #     os.makedirs(tar_dir)
    temps = list(itertools.combinations(name_list, num))
    for j in range(len(temps)):
        new_segment_path = tar_dir + '_' + str(j) + '/'
        if not os.path.exists(new_segment_path):
            os.makedirs(new_segment_path)
        for name in temps[j]:
            shutil.copyfile(file_dir + name + '.txt', new_segment_path + name + '.txt')


def sample_file(file_dir, tar_dir, num):
    path_dir = os.listdir(file_dir)
    if not os.path.exists(tar_dir):
        os.makedirs(tar_dir)
    sample = random.sample(path_dir, num)
    for name in sample:
        shutil.copytree(file_dir + name, tar_dir + name)


def merge_all_sample(split_path, file_out, label_out):
    fileout = open(file_out, 'a+')
    labelout = open(label_out, 'a+')
    file_lists = os.listdir(split_path)
    file_lists = random.shuffle(file_lists)
    for name in file_lists:
        labelout.write(name)
        labelout.write(' ')
        with open(split_path + name + '.txt') as f:
            text = f.read()
            fileout.write(text)
        fileout.write('\n')
        fileout.write('\n')
    labelout.write('\n')
    fileout.flush()
    fileout.close()
    labelout.flush()
    labelout.close()


if __name__ == '__main__':
    fileDir = './test/origin/'  # source path
    tarDir = './test/new/'  # target path
    sample_tarDir = './data/new_1/'
    sample_num = 200  # the number of samples you want
    file_path_dir = os.listdir(fileDir)
    print(file_path_dir)
    for file_path in file_path_dir:
        # candidate facet labels == names of the segment files
        namelist = ['algorithm', 'application', 'definition', 'example', 'property',
                    'history', 'implementation', 'method', 'operation', 'type']
        arr = [3, 4, 5, 6, 7, 8]  # change this list to decide your own reorganized data
        for i in range(len(arr)):
            reorganize(fileDir + file_path + '/', tarDir + str(arr[i]) + '_' + file_path, namelist, arr[i])
    sample_file(tarDir, sample_tarDir, sample_num)
