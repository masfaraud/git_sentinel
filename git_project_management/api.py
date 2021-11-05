#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 08:39:49 2021

@author: steven
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

app.config['CORS_EXPOSE_HEADERS'] = ['Content-Disposition']
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Before inserting config
cors = CORS(app)


# Read from env vars
for env_var_name in ['DB_HOST', 'DB_USER', 'DB_NAME', 'DB_PASSWORD', 'DB_PORT']:
    if env_var_name in os.environ and os.environ[env_var_name]:
        app.config[env_var_name] = os.environ[env_var_name]
    else:
        raise RuntimeError('Could not load {} from env vars'.format(env_var_name))

import git_project_management.models as gpm_models

project_manager = gpm_models.ProjectManager(app.config['DB_HOST'],
                                            app.config['DB_PORT'],
                                            app.config['DB_USER'],
                                            app.config['DB_NAME'],
                                            app.config['DB_PASSWORD'])

# Enhance this with a sync route!
# print('updating infos')
# project_manager.update()
# print('done')

from git_project_management import __version__
import git_project_management.routes



@app.route('/')
def index():
    # vinfo = sys.version_info

    # if _tasks_loaded:
    #     celery_workers = tasks.celery_workers()
    # else:
    #     celery_workers = []

    return jsonify({'api_version': __version__})
