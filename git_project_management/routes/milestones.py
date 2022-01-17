#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 19:37:40 2022

@author: steven
"""

import pony.orm

from flask import jsonify, request
from git_project_management.api import app
from git_project_management.models import Milestone


@app.route('/milestones')
@pony.orm.db_session()
def list_milestones():
    milestones = [m.to_dict() for m in Milestone.select()]
    
    return jsonify({'milestones': milestones})


@app.route('/milestones/<int:milestone_id>')
@pony.orm.db_session()
def milestone_details(milestone_id):

    milestone = Milestone.get(id=milestone_id)
    if not milestone:
        return 'No such milestone', 404
    
    return jsonify(milestone.to_dict(full_infos=True))


