#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 18:52:57 2022

@author: steven
"""

import pony.orm

from flask import jsonify, request
from git_sentinel.api import app
from git_sentinel.models import GitPlatform


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

    query = GitPlatform.select()

    if asc_order:
        items = query.order_by(getattr(GitPlatform, order_by))
    else:
        items = query.order_by(pony.orm.desc(getattr(GitPlatform, order_by)))

    return jsonify({'platforms': [i.to_dict() for i in items],
                    'limit': limit,
                    'offset': offset})


@app.route('/platforms/<int:platform_id>')
@pony.orm.db_session()
def platforms_details(platform_id):

    platform = GitPlatform.get(id=platform_id)
    if not platform:
        return 'No such platform', 404

    return jsonify(platform.to_dict())
