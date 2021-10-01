#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 17:19:04 2021

@author: steven
"""

import git_project_management.models as gpm_models
import config as conf

project_manager = gpm_models.ProjectManager(conf.db_host, conf.db_port,
                                     conf.db_user, conf.db_name, conf.db_password)

project_manager.update()
project_manager.plot_issues()