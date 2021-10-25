#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 09:10:44 2021

@author: steven
"""

import pony.orm
from flask import jsonify 
from git_project_management.api import app
from git_project_management.models import Repository


@app.route('/repositories')
@pony.orm.db_session()
def list_repos():

    repos = [r.to_dict() for r in Repository.select()]
    
    return jsonify({'repositories': repos})
