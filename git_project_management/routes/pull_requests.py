#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 17:15:51 2021

@author: steven
"""


import pony.orm

from flask import jsonify, request
from git_project_management.api import app
from git_project_management.models import PullRequest


@app.route('/pull-requests')
@pony.orm.db_session()
def list_pr():
    order_by = request.args.get('order_by', type=str, default='id')
    limit = request.args.get('limit', type=int, default=10)
    offset = request.args.get('offset', type=int, default=0)
    
    asc_order = True
    if ':' in order_by:
        order_by, asc_order = order_by.split('.')
        asc_order = asc_order == 'asc'
        
    state = request.args.get('state', type=str, default='open')
    if state == 'all':
        query = PullRequest.select()
    else:
        merged = state == 'merged'
        query = PullRequest.select(lambda i: i.merged == merged)
    
    if asc_order:
        prs = query.order_by(getattr(PullRequest, order_by))
    else:
        prs = query.order_by(pony.orm.desc(getattr(PullRequest, order_by)))
    
    return jsonify({'pull_requests': [i.to_dict() for i in prs],
                    'limit': limit,
                    'offset': offset})


@app.route('/pull-requests/<int:pull_request_id>')
@pony.orm.db_session()
def pr_details(pull_request_id):

    pr = PullRequest.get(id=pull_request_id)
    if not pr:
        return 'No such issue', 404
    
    return jsonify(pr.to_dict())