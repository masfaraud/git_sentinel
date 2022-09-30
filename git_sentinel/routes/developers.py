#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:28:21 2021

@author: steven
"""

import pony.orm

from flask import jsonify, request
from git_sentinel.api import app
from git_sentinel.models import Developer


@app.route('/developers')
@pony.orm.db_session()
def list_devs():
    order_by = request.args.get('order_by', type=str, default='id')
    limit = request.args.get('limit', type=int, default=10)
    offset = request.args.get('offset', type=int, default=0)
    
    asc_order = True
    if ':' in order_by:
        order_by, asc_order = order_by.split('.')
        asc_order = asc_order == 'asc'
        
    query = Developer.select()
    
    if asc_order:
        issues = query.order_by(getattr(Developer, order_by))
    else:
        issues = query.order_by(pony.orm.desc(getattr(Developer, order_by)))
    
    # TOdo : limit offset
    
    return jsonify({'developers': [i.to_dict() for i in issues],
                    'limit': limit,
                    'offset': offset})

@app.route('/developers/<int:developer_id>')
@pony.orm.db_session()
def developer_details(developer_id):

    dev = Developer.get(id=developer_id)
    if not dev:
        return 'No such developer', 404
    
    return jsonify(dev.to_dict(full_infos=True))