#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:28:21 2021

@author: steven
"""

import pony.orm

from flask import jsonify, request
from git_project_management.api import app
from git_project_management.models import Issue


@app.route('/issues')
@pony.orm.db_session()
def list_issues():
    state = request.args.get('state', type=str, default='open')
    if state == 'all':
        req = Issue.select()
    else:
        closed = state == 'closed'
        req = Issue.select(lambda i: i.closed == closed)
    
    issues = req.order_by(Issue.created_at)
    
    return jsonify({'issues': [i.to_dict() for i in issues]})


@app.route('/issues/<int:issue_id>')
@pony.orm.db_session()
def issue_details(issue_id):

    issue = Issue.get(id=issue_id)
    if not issue:
        return 'No such issue', 404
    
    return jsonify(issue.to_dict())