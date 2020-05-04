# -*- coding: utf-8 -*-
# Time : 2020/4/14 18:35
# Author : Shuo Chang
# File : train_and_test.py
# Software: WeatherPrediction

"""Train xgboost model and Test for very verification."""

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys

import math
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from citybuster.utils.logging import setup_logging

logger = setup_logging(__name__, '../log', 'train_test.txt')


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train and Test"
    )
    parser.add_argument(
        "--data", dest="data_path", help="data file path", default=None, type=str
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    ret = parser.parse_args()
    if not os.path.isfile(ret.data_path):
        logger.warning("The excel file path is not correct.")
        sys.exit(-1)

    return ret


def train(X_train, y_train):
    xgdmat = xgb.DMatrix(X_train, y_train)
    our_params = {'eta': 0.8, 'seed': 1, 'gamma': 0.1, 'subsample': 0.9, 'colsample_bytree': 0.9,
                  'objective': 'reg:squarederror', 'max_depth': 16, 'min_child_weight': 1}

    final_gb = xgb.train(our_params, xgdmat)

    return final_gb


def test(model, X_test, y_test):
    tesdmat = xgb.DMatrix(X_test)
    y_pred = model.predict(tesdmat)

    abs_values = np.absolute(y_test.values - y_pred)
    abs_values = abs_values <= 2
    success_ratio = np.sum(abs_values)/abs_values.size
    test_score = math.sqrt(mean_squared_error(y_test.values, y_pred))

    return y_pred, test_score, success_ratio


def run(input_data, label, mode='High'):
    # Prepare high temperature train test data
    X_train, X_test, y_train, y_test = train_test_split(input_data, label, test_size=0.1, random_state=42)

    # Train model
    logger.info(mode + ' Train Start:')
    regression_model = train(X_train, y_train)
    logger.info('Done')

    # Test model
    logger.info(mode + ' Test Start:')
    _, _, success_ratio = test(regression_model, X_test, y_test)
    logger.info('Done')

    return success_ratio


def main():
    args = parse_args()
    logger.info("Called with args:")
    logger.info(args)

    # Load data
    data = pd.read_csv(args.data_path)
    input_data = data.drop(['id', 'HT', 'LT'], axis=1)
    high_temperature_label = data.pop('HT')
    low_temperature_label = data.pop('LT')

    # Evaluate High
    logger.info('Evaluate High')
    success_ratio = run(input_data, high_temperature_label)
    print('High Success ratio is: %f' % success_ratio)

    # Evaluate Low
    logger.info('Evaluate Low')
    success_ratio = run(input_data, low_temperature_label, mode='Low')
    print('High Success ratio is: %f' % success_ratio)


if __name__ == "__main__":
    main()
