# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Email
------------      -------    --------    -----------
2022/9/7 19:28   zhangcy      1.0       zf2113106@buaa.edu.cn
"""
import sys
import os
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from pandas.core.frame import DataFrame
import time
import xlwt
import matplotlib as mpl
from numpy import genfromtxt


def loading_data(file_dir, file_name):
    '''
    加载数据
    :param file_dir:数据存储文件夹
    :param file_name:要打开的数据文件，默认为空，为空则打开文件夹内的所有文件并合并
    :param auto_drive_values:是否含有自动驾驶的标志位
    :return:加载后的数据
    '''
    if len(file_name) == 0:
        all_csv_list = os.listdir(file_dir)
        for single_csv in all_csv_list:
            single_dataframe = pd.read_csv(os.path.join(file_dir, single_csv))
            if single_csv == all_csv_list[0]:
                all_dataframe = single_dataframe
            else:
                all_dataframe = pd.concat([all_dataframe, single_dataframe], ignore_index=1, sort=True)
    else:
        path = file_dir + file_name
        single_csv = open(path, encoding='utf-8')
        single_dataframe = pd.read_csv(single_csv)
        all_dataframe = single_dataframe
    return all_dataframe


def cal_val(part_len, part_point, data_relative, remainder_flag=0, remainder_point=0):
    dict_crs = {"type": "name",
                "properties": {"name": "urn:ogc:def:crs:EPSG::32610"}}
    dict_geometry_empty = {}

    # 对每个片段进行操作
    if remainder_flag == 0:
        list_features = [{"geometry": dict_geometry_empty,
                          "type": "Feature",
                          "properties": {
                              "right_id": 0,
                              "left_id": 0,
                              "rchg_vld": 0,
                              "length": 0,
                              "father_id": "0",
                              "behavior": "s",
                              "child_id": "0",
                              "lchg_vld": 0,
                              "id": 1}}] * int(len(data_relative) / 40)
        for i in range(part_point):
            list_coordinates = [[0, 0]] * part_len  # 初始化坐标列表
            # 对一个片段中的40个数据点进行操作
            for j in range(part_len * i, part_len * (i + 1)):
                list_coordinates[j - part_len * i] = [data_relative[j, 0], data_relative[j, 1]]

            dict_geometry = {"type": "MultiLineString",
                             "coordinates": [list_coordinates]}
            length = math.sqrt(
                pow(list_coordinates[part_len - 1][0] - list_coordinates[0][0], 2)
                + pow(list_coordinates[part_len - 1][1] - list_coordinates[0][1], 2))  # 通过首尾两个点计算长度
            if i == 0:
                father_id = 0
            else:
                father_id = i - 1
            father_id_str = str(father_id)
            if i == part_point - 1:
                child_id = 0
            else:
                child_id = i + 1
            child_id_str = str(child_id)
            self_id = i
            list_features[i] = {"geometry": dict_geometry,
                                "type": "Feature",
                                "properties": {
                                    "right_id": 0,
                                    "left_id": 0,
                                    "rchg_vld": 0,
                                    "length": length,
                                    "father_id": father_id_str,
                                    "behavior": "s",
                                    "child_id": child_id_str,
                                    "lchg_vld": 0,
                                    "id": self_id}
                                }
    else:
        list_features = [{"geometry": dict_geometry_empty,
                          "type": "Feature",
                          "properties": {
                              "right_id": 0,
                              "left_id": 0,
                              "rchg_vld": 0,
                              "length": 0,
                              "father_id": "0",
                              "behavior": "s",
                              "child_id": "0",
                              "lchg_vld": 0,
                              "id": 1}}] * (int(len(data_relative) / 40) + 1)
        for i in range(part_point):
            list_coordinates = [[0, 0]] * part_len  # 初始化坐标列表
            # 对一个片段中的40个数据点进行操作
            for j in range(part_len * i, part_len * (i + 1)):
                list_coordinates[j - part_len * i] = [data_relative[j, 0], data_relative[j, 1]]

            dict_geometry = {"type": "MultiLineString",
                             "coordinates": [list_coordinates]}
            length = math.sqrt(
                pow(list_coordinates[part_len - 1][0] - list_coordinates[0][0], 2)
                + pow(list_coordinates[part_len - 1][1] - list_coordinates[0][1], 2))  # 通过首尾两个点计算长度
            if i == 0:
                father_id = 0
            else:
                father_id = i - 1
            father_id_str = str(father_id)
            if i == part_point - 1:
                child_id = 0
            else:
                child_id = i + 1
            child_id_str = str(child_id)
            self_id = i
            list_features[i] = {"geometry": dict_geometry,
                                "type": "Feature",
                                "properties": {
                                    "right_id": 0,
                                    "left_id": 0,
                                    "rchg_vld": 0,
                                    "length": length,
                                    "father_id": father_id_str,
                                    "behavior": "s",
                                    "child_id": child_id_str,
                                    "lchg_vld": 0,
                                    "id": self_id}
                                }
        i = part_point
        list_coordinates = [[0, 0]] * remainder_point  # 初始化坐标列表
        # 对一个片段中的40个数据点进行操作
        for j in range(part_len * i, part_len * i + remainder_point):
            list_coordinates[j - part_len * i] = [data_relative[j, 0], data_relative[j, 1]]

        dict_geometry = {"type": "MultiLineString",
                         "coordinates": [list_coordinates]}
        length = math.sqrt(
            pow(list_coordinates[remainder_point - 1][0] - list_coordinates[0][0], 2)
            + pow(list_coordinates[remainder_point - 1][1] - list_coordinates[0][1], 2))  # 通过首尾两个点计算长度
        if i == 0:
            father_id = 0
        else:
            father_id = i - 1
        father_id_str = str(father_id)
        if i == part_point - 1:
            child_id = 0
        else:
            child_id = i + 1
        child_id_str = str(child_id)
        self_id = i
        list_features[i] = {"geometry": dict_geometry,
                            "type": "Feature",
                            "properties": {
                                "right_id": 0,
                                "left_id": 0,
                                "rchg_vld": 0,
                                "length": length,
                                "father_id": father_id_str,
                                "behavior": "s",
                                "child_id": child_id_str,
                                "lchg_vld": 0,
                                "id": self_id}
                            }
    dict_lane = {"crs": dict_crs,
                 "type": "FeatureCollection",
                 "name": "hw_01_lane_re_sm2",
                 "features": list_features}
    return dict_lane


def main():
    # 解析csv文件
    # 读取数据并筛选补零，按照范围截取数据
    file_path = sys.argv[1]  # 命令行中传入的数据地址
    data = loading_data(file_path, 'demo.csv')
    data = data.iloc[0:, 5:7]  # 只保留道路转换后的坐标
    data_array = np.array(data)  # 转换为array

    data_relative = np.zeros((len(data_array), 2))
    #
    # 将坐标减去第一个坐标值，生成相对坐标值
    for i in range(len(data)):
        for j in [0, 1]:
            data_relative[i, j] = data_array[i, j] - data_array[0, j]
            # print(data_relative[i, j])

    # 解析json文件
    # 读json文件
    # with open('./highway_v1.0/lane_net_norm_1.json') as f:
    #     data = json.load(f)

    # data_features = data['features']  # 列表
    # for i in range(len(data_features)):
    #     # data_features[i]包含geometry、type、properties
    #     data_geometry = data_features[i]['geometry']
    #     data_type = data_features[i]['type']
    #     data_properties = data_features[i]['properties']
    #
    #     # data_properties字典
    #     data_right_id = data_properties['right_id']
    #     data_left_id = data_properties['left_id']
    #     data_rchg_vld = data_properties['rchg_vld']
    #     data_lchg_vld = data_properties['lchg_vld']
    #     data_length = data_properties['length']
    #     data_father_id = data_properties['father_id']
    #
    #     data_behavior = data_properties['behavior']
    #     data_child_id = data_properties['child_id']
    #
    #     # print(type(data_features[i]))

    # 每40个点放到一个coordinates字典中
    part_len = 40
    if len(data_relative) % part_len == 0:
        dict_lane = cal_val(part_len, int(len(data_relative) / part_len), data_relative)
    else:
        remainder_point = len(data_relative) % part_len  # 记录余数
        dict_lane = cal_val(part_len, int(len(data_relative) / part_len), data_relative, remainder_flag=1,
                            remainder_point=remainder_point)

    # 写json文件
    with open('./highway_v1.0/lane_net_norm_2.json', 'w') as wf:
        json.dump(dict_lane, wf, indent=4, ensure_ascii=False)


main()
