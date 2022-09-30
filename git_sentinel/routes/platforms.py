#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 18:52:57 2022

@author: steven
"""

import pony.orm

from flask import jsonify, request
from git_sentinel.api import app
from git_sentinel.models import Issue


@app.route('/platforms')
@pony.orm.db_session()
def list_platforms():
    order_by = request.args.get('order_by', type=str, default='id')
    limit = request.args.get('limit', type=int, default=10)
    offset = request.args.get('offset', type=int, default=0)
    
    asc_order = True
    if ':' in order_by:
        order_by, asc_order = order_by.split('.')
        asc_order = asc_order == 'asc'
        
    state = request.args.get('state', type=str, default='open')
    if state == 'all':
        query = Issue.select()
    else:
        closed = state == 'closed'
        query = Issue.select(lambda i: i.closed == closed)
    
    if asc_order:
        issues = query.order_by(getattr(Issue, order_by))
    else:
        issues = query.order_by(pony.orm.desc(getattr(Issue, order_by)))
    
    return jsonify({'issues': [i.to_dict() for i in issues],
                    'limit': limit,
                    'offset': offset})
