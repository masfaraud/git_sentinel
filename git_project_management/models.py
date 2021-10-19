#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3
"""

"""
import datetime
import ciso8601
import pony.orm
import requests

import matplotlib.pyplot as plt

pony_db = pony.orm.Database()

class GitPlatform(pony_db.Entity):
    base_url = pony.orm.Required(str, 100, unique=True)
    token = pony.orm.Required(str, 100)
    
    @property
    def api_url(self):
        return '{}/api/v1'.format(self.base_url)

class GithubPlatform(GitPlatform):
    username = pony.orm.Required(str, 100, unique=True)
    # token = pony.orm.Required(str, 100)
    
    
class GiteaPlatform(GitPlatform):
    repositories = pony.orm.Set('GiteaRepository')

    @pony.orm.db_session()
    def get_repos(self):
        req = requests.get('{}/user/repos'.format(self.api_url),
                           params={'access_token': self.token})
        for req_issue in req.json():
            print(req_issue['name'])
            
            # print('req_issue', req_issue)
            owner_name = req_issue['owner']['username']
            repo = GiteaRepository.get(platform=self,
                                       name=req_issue['name'],
                                       owner=owner_name,
                                       )
            if not repo:
                repo = GiteaRepository(platform=self,
                                       name=req_issue['name'],
                                       owner=owner_name
                              )
            else:
                repo.name = req_issue['name']
                repo.owner = owner_name
    
    @pony.orm.db_session()
    def get_issues(self):
        for repo in self.repositories:
            repo.get_issues()
                
class Repository(pony_db.Entity):
    name = pony.orm.Required(str, 255)
    issues = pony.orm.Set('Issue')
    active = pony.orm.Required(bool, default=False)
    pull_requests = pony.orm.Set('PullRequest')
    milestones = pony.orm.Set('Milestone')

    def __str__(self):
        return self.owner + '.' + self.name

    @pony.orm.db_session()
    def plot_issues(self, weeks=15):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        labels = []
        open_issues = []
        new_issues = []
        closed_issues = []
        
        now = datetime.datetime.now()
        for iw in range(weeks):
            week_start = (now - datetime.timedelta(weeks=iw+1)).timestamp()
            week_end = (now - datetime.timedelta(weeks=iw)).timestamp()
            
            open_issues_week = self.issues.select(lambda i:i.created_at<week_end and (not i.closed or i.closed_at>week_end))
            new_issues_week = self.issues.select(lambda i:i.created_at>week_start and i.created_at<week_end)
            closed_issues_week = self.issues.select(lambda i:i.closed_at<week_end and i.closed_at>week_start)
            
            open_issues.append(open_issues_week.count())
            new_issues.append(new_issues_week.count())
            closed_issues.append(closed_issues_week.count())
            labels.append((now - datetime.timedelta(weeks=iw+1)).strftime('W%U %Y'))
            

        r_labels = labels[::-1]
        
        r_closed_issues = closed_issues[::-1]
        r_new_issues = new_issues[::-1]
        r_open_issues = open_issues[::-1]

        ax1.bar(r_labels, r_closed_issues, label='closed in the week', color='r', align='edge')
        ax1.bar(r_labels, r_new_issues, bottom=r_closed_issues,
               label='new in the week', color='g', align='edge')
        # print(str(self))
        ax1.legend()

        ax2.bar(r_labels, r_open_issues, label='Open issues', color='g', align='edge')
        ax2.legend()

        ax1.set_title(str(self))

class GiteaRepository(Repository):
    platform = pony.orm.Required(GiteaPlatform)
    owner = pony.orm.Required(str, 100)
    
    @pony.orm.db_session()
    def get_issues(self):
        page_number_issues = 1
        page_number = 1
        while page_number_issues:
            print('page', page_number)
            req = requests.get('{}/repos/{}/{}/issues'.format(self.platform.api_url, self.owner, self.name),
                               params={'state':'all',
                                       'page': page_number,
                                       'access_token': self.platform.token})
            for req_issue in req.json():
                issue = Issue.get(repository=self,
                                  number=req_issue['number'])
                created_at = int(ciso8601.parse_datetime(req_issue['created_at']).timestamp())
                updated_at = int(ciso8601.parse_datetime(req_issue['updated_at']).timestamp())
                closed = req_issue['state']=='closed'
                
                if not issue:
                    issue = Issue(number=req_issue['number'],
                                  repository=self,
                                  title=req_issue['title'],
                                  body=req_issue['body'],
                                  api_url=req_issue['url'],
                                  html_url=req_issue['html_url'],
                                  closed=closed,
                                  created_at=created_at,
                                  updated_at=updated_at
                                  )
                else:
                    issue.title = req_issue['title']
                    issue.body = req_issue['body']
                    issue.closed = closed
    
                if req_issue['milestone']:
                    print(req_issue['milestone'])
                    milestone = Milestone.get(platform_id=req_issue['milestone']['id'])
                    if not milestone:


                        milestone = Milestone(platform_id=req_issue['milestone']['id'],
                                              repository = self,
                                              title = req_issue['milestone']['title'])
                                              
                    if 'due_on' in req_issue['milestone'] and req_issue['milestone']['due_on']:
                        milestone.due_on = int(ciso8601.parse_datetime(req_issue['milestone']['due_on']).timestamp())
                        
                    if req_issue['milestone']['closed_at']:
                        milestone.closed_at = int(ciso8601.parse_datetime(req_issue['milestone']['closed_at']).timestamp())
                        
                    if not issue in milestone.issues:
                        milestone.issues.add(issue)
    
                if req_issue['closed_at']:
                    issue.closed_at = int(ciso8601.parse_datetime(req_issue['closed_at']).timestamp())
    
            page_number_issues = len(req.json())
            page_number += 1

    @pony.orm.db_session()
    def get_pull_requests(self):
        req = requests.get('{}/repos/{}/{}/pulls'.format(self.platform.api_url, self.owner, self.name),
                           params={'state':'all',
                                   'access_token': self.platform.token})
        for req_pr in req.json():
            pull_request = PullRequest.get(repository=self,
                                           number=req_pr['number'])
            created_at = int(ciso8601.parse_datetime(req_pr['created_at']).timestamp())
            updated_at = int(ciso8601.parse_datetime(req_pr['updated_at']).timestamp())
            merged = req_pr['merged']=='true'
            
            
            if not pull_request:
                pull_request = PullRequest(number=req_pr['number'],
                                           repository=self,
                                           title=req_pr['title'],
                                           body=req_pr['body'],
                                           api_url=req_pr['url'],
                                           html_url=req_pr['html_url'],
                                           merged=merged,
                                           created_at=created_at,
                                           updated_at=updated_at,
                                           base_branch=req_pr['base']['label'],
                                           head_branch=req_pr['head']['label'],
                                    )
            else:
                pull_request.title = req_pr['title']
                pull_request.body = req_pr['body']
                pull_request.merged = merged      
    
            if req_pr['merged_at']:
                pull_request.merged_at = int(ciso8601.parse_datetime(req_pr['merged_at']).timestamp())
    
class Issue(pony_db.Entity):
    number = pony.orm.Required(int)
    repository = pony.orm.Required(Repository)
    title = pony.orm.Required(str, 255)
    body = pony.orm.Optional(str, 50000)
    api_url = pony.orm.Required(str, 255)
    html_url = pony.orm.Required(str, 255)
    closed = pony.orm.Required(bool, default=False)
    created_at = pony.orm.Required(int)
    updated_at = pony.orm.Required(int)
    closed_at = pony.orm.Optional(int)
    milestone = pony.orm.Optional('Milestone')
    
class PullRequest(pony_db.Entity):
    number = pony.orm.Required(int)
    repository = pony.orm.Required(Repository)
    title = pony.orm.Required(str, 255)
    base_branch = pony.orm.Required(str, 255)
    head_branch = pony.orm.Required(str, 255)
    body = pony.orm.Optional(str, 50000)
    api_url = pony.orm.Required(str, 255)
    html_url = pony.orm.Required(str, 255)
    merged = pony.orm.Required(bool, default=False)
    mergeable = pony.orm.Required(bool, default=False)
    created_at = pony.orm.Required(int)
    merged_at = pony.orm.Optional(int)
    updated_at = pony.orm.Required(int)
    
class Milestone(pony_db.Entity):
    platform_id = pony.orm.Required(int)
    closed_at = pony.orm.Optional(int)
    repository = pony.orm.Required(Repository)
    title = pony.orm.Required(str, 255)
    issues = pony.orm.Set(Issue)
    due_on = pony.orm.Optional(int)

    
    
class ProjectManager:
    def __init__(self, db_host, db_port, db_user, db_name, db_password):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_name = db_name
        self.db_password = db_password
        
        pony_db.bind(provider='mysql', host=self.db_host, user=self.db_user,
                passwd=self.db_password, db=self.db_name)
        pony_db.generate_mapping(create_tables=True)

    @pony.orm.db_session()
    def add_gitea_platform(self, base_url, token):
        platform = GiteaPlatform(base_url=base_url, token=token)
        return platform
    
    @pony.orm.db_session()
    def get_platforms(self):
        return list(GitPlatform.select())


    @pony.orm.db_session()
    def active_repositories(self):
        return list(Repository.select(lambda r:r.active))    
    
    @pony.orm.db_session()
    def update(self):
        # print('global update')
        for platform in GitPlatform.select():
            # print('platform', platform)
            platform.get_repos()
        for repo in Repository.select(lambda r:r.active):
            # print(repo)
            repo.get_issues()
            repo.get_pull_requests()
    
    # @property
    # def issues(self):
    #     return Issue.select(lambda i:True)
    
    # @pony.orm.db_session()
    # def plot_issues(self, weeks=12):
    #     Repository.plot_issues(self)
       
