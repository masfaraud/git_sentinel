#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 17:37:07 2021

@author: steven
"""

import pkg_resources

__version__ = pkg_resources.require("git_sentinel")[0].version
