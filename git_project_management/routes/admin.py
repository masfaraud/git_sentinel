#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 18:40:52 2022

@author: steven
"""

import pony.orm

from flask import jsonify, request
from git_project_management.api import app, project_manager
# from git_project_management.models import Issue


@app.route('/admin/update')
@pony.orm.db_session()
def update():
    project_manager.update()
    return jsonify({'message': 'Update performed.'})