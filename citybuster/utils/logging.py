# -*- coding: utf-8 -*-
# Time : 2020/4/11 12:26
# Author : Shuo Chang
# File : logging.py
# Software: WeatherPrediction


from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os
import sys


def setup_logging(name, save_dir, filename="log.txt"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if save_dir:
        if os.path.isfile(os.path.join(save_dir, filename)):
            os.remove(os.path.join(save_dir, filename))
        fh = logging.FileHandler(os.path.join(save_dir, filename))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
