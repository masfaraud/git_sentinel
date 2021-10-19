#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 17:19:04 2021

@author: steven
"""

import pony
import git_project_management.models as gpm_models
import config as conf

project_manager = gpm_models.ProjectManager(conf.db_host, conf.db_port,
                                     conf.db_user, conf.db_name, conf.db_password)
with pony.orm.db_session:
    
    # project_manager.update()
    # project_manager.plot_issues()
    # for platform in project_manager.get_platforms():
    #     for repo in platform.repositories:
    #         if repo.owner == 'DessiA' and not repo.active:
    #             print(repo.owner, '/', repo.name, repo.active)
    #             active = input('Activate (y/n)')
    #             if active == 'y':
    #                 repo.active = True
            
            
    for repo in project_manager.active_repositories():
        # print(repo.title)
        repo.plot_issues()
        repo.plot_milestones()
        