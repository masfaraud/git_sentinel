#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 09:10:44 2021

@author: steven
"""

import pony.orm

from flask import jsonify, request
from git_sentinel.api import app
from git_sentinel.models import Repository


@app.route('/repositories')
@pony.orm.db_session()
def list_repos():
    only_active = request.args.get('only_active', type=bool, default=True)
    if only_active:
        repos = [r.to_dict() for r in Repository.select(lambda r:r.active)]
    else:
        repos = [r.to_dict() for r in Repository.select()]
    
    return jsonify({'repositories': repos})


@app.route('/repositories/<int:repo_id>')
@pony.orm.db_session()
def repo_details(repo_id):

    repo = Repository.get(id=repo_id)
    if not repo:
        return 'No such repo', 404
    
    return jsonify(repo.to_dict(stats=True, full_infos=True))


