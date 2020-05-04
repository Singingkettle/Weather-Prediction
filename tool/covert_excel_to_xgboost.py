# -*- coding: utf-8 -*-
# Time : 2020/4/11 12:20
# Author : Shuo Chang
# File : covert_excel_to_xgboost.py
# Software: WeatherPrediction

"""Convert the excel data file to xgboost format. And prepare the dataset for prediction model."""

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys

import pandas as pd

from citybuster.utils.logging import setup_logging

logger = setup_logging(__name__, '../log', 'convert.txt')

__SHEET_LIST = ['2018-2019', ]
__SPLIT_RATIO = {'train': 0.5, 'validation': 0.2, 'test': 0.3}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert an excel to xgboost format"
    )
    parser.add_argument(
        "--excel", dest="excel_file", help="excel file data path", default=None, type=str
    )
    parser.add_argument(
        "--key", dest="key_file", help="keys of input variables", default=None, type=str
    )
    parser.add_argument(
        "--save", dest="save_folder", help="folder to save the converted results", default=None, type=str
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    ret = parser.parse_args()
    if not os.path.isfile(ret.excel_file):
        logger.warning("The excel file path is not correct.")
        sys.exit(-1)

    if not os.path.isdir(ret.save_folder):
        logger.warning("The save folder is not existent.")
        sys.exit(-1)

    return ret


def save_as_csv(save_path, item_list):
    pf = pd.DataFrame(data=item_list)
    pf.to_csv(save_path, encoding="utf-8-sig", mode="a", header=False, index=False)


def convert_and_split(args):
    excel_file = args.excel_file
    xl = pd.ExcelFile(excel_file)
    df = xl.parse(__SHEET_LIST[0])

    # Load the key file
    with open(args.key_file, 'r') as f:
        line = f.readline()
        line = line.strip()
        keys = line.split(',')

    # Extract data and save as xgboost (csv) format
    save_path = os.path.join(args.save_folder, 'data.csv')
    if os.path.isfile(save_path):
        os.remove(save_path)

    logger.info("Start Converting:")
    id_index = 0
    for row in df.itertuples():
        if getattr(row, 'hour') == "12时":
            item_list = [id_index]
            for key in keys[1:]:
                item_list.append(getattr(row, key))
            save_as_csv(save_path, [item_list])
            id_index += 1
    keys[0] = 'id'
    df = pd.read_csv(save_path, header=None, names=keys)
    df.to_csv(save_path, index=False)
    logger.info("Done!")


def main():
    args = parse_args()
    logger.info("Called with args:")
    logger.info(args)

    # Convert the excel file to xgboost format and split
    convert_and_split(args)


if __name__ == "__main__":
    main()
