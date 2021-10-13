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

    def __str__(self):
        return self.owner + '.' + self.name

    @pony.orm.db_session()
    def plot_issues(self, weeks=10):
        labels = []
        open_issues = []
        new_issues = []
        closed_issues = []
        now = datetime.datetime.now()
        for iw in range(weeks):
            week_start = (now - datetime.timedelta(weeks=iw+1)).timestamp()
            week_end = (now - datetime.timedelta(weeks=iw)).timestamp()
            open_issues_week = self.issues.select(lambda i:i.created_at<week_end and i.closed_at>week_end)
            new_issues_week = self.issues.select(lambda i:i.created_at>week_start and i.created_at<week_end)
            closed_issues_week = self.issues.select(lambda i:i.closed_at<week_end and i.closed_at>week_start)
            
            open_issues.append(open_issues_week.count())
            new_issues.append(new_issues_week.count())
            closed_issues.append(closed_issues_week.count())
            labels.append((now - datetime.timedelta(weeks=iw+1)).strftime('W%U %Y'))
            
        fig, ax = plt.subplots()

        r_labels = labels[::-1]
        r_closed_issues = closed_issues[::-1]
        r_new_issues = new_issues[::-1]

        ax.bar(r_labels, r_closed_issues, label='closed', color='r', align='edge')
        ax.bar(r_labels, r_new_issues, bottom=r_closed_issues,
               label='new', color='g', align='edge')
        # print(str(self))
        ax.set_title(str(self))
        ax.legend()

class GiteaRepository(Repository):
    platform = pony.orm.Required(GiteaPlatform)
    owner = pony.orm.Required(str, 100)
    
    @pony.orm.db_session()
    def get_issues(self):
        req = requests.get('{}/repos/{}/{}/issues'.format(self.platform.api_url, self.owner, self.name),
                           params={'state':'all',
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

            if req_issue['closed_at']:
                issue.closed_at = int(ciso8601.parse_datetime(req_issue['closed_at']).timestamp())

    @pony.orm.db_session()
    def get_pull_requests(self):
        req = requests.get('{}/repos/{}/{}/pulls'.format(self.platform.api_url, self.owner, self.name),
                           params={'state':'all',
                                   'access_token': self.platform.token})
        for req_pr in req.json():
            pull_request = PullRequest.get(repository=self,
                                           number=req_pr['number'])
            created_at = int(ciso8601.parse_datetime(req_pr['created_at']).timestamp())
            merged_at = int(ciso8601.parse_datetime(req_pr['merged_at']).timestamp())
            merged = req_pr['merged']=='true'
            
            # if not pull_request:
            #     issue = Issue(number=req_issue['number'],
            #                   repository=self,
            #                   title=req_issue['title'],
            #                   body=req_issue['body'],
            #                   api_url=req_issue['url'],
            #                   html_url=req_issue['html_url'],
            #                   closed=closed,
            #                   created_at=created_at,
            #                   updated_at=updated_at
            #                   )
            # else:
            #     issue.title = req_issue['title']
            #     issue.body = req_issue['body']
            #     issue.closed = closed      
    
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
    
    
class PullRequest(pony_db.Entity):
    number = pony.orm.Required(int)
    repository = pony.orm.Required(Repository)
    # title = pony.orm.Required(str, 255)
    body = pony.orm.Optional(str, 50000)
    api_url = pony.orm.Required(str, 255)
    html_url = pony.orm.Required(str, 255)
    merged = pony.orm.Required(bool, default=False)
    mergeable = pony.orm.Required(bool, default=False)
    created_at = pony.orm.Required(int)
    merged_at = pony.orm.Optional(int)
        
# class Milestone(pony_db.Entity):
    
#     issues = pony.orm.Set(Issue)
    
    
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
        print('global update')
        for platform in GitPlatform.select():
            print('platform', platform)
            platform.get_repos()
        for repo in Repository.select(lambda r:r.active):
            # print(repo)
            repo.get_issues()
    
    @pony.orm.db_session()
    def plot_issues(self, weeks=12):
        labels = []
        open_issues = []
        new_issues = []
        closed_issues = []
        now = datetime.datetime.now()
        for i in range(weeks):
            week_start = (now - datetime.timedelta(weeks=i+1)).timestamp()
            week_end = (now - datetime.timedelta(weeks=i)).timestamp()
            open_issues_week = Issue.select(lambda i:i.created_at<week_end and i.closed_at>week_end)
            new_issues_week = Issue.select(lambda i:i.created_at>week_start and i.created_at<week_end)
            closed_issues_week = Issue.select(lambda i:i.closed_at<week_end and i.closed_at>week_start)
            
            open_issues.append(open_issues_week.count())
            new_issues.append(new_issues_week.count())
            closed_issues.append(closed_issues_week.count())
            labels.append((now - datetime.timedelta(weeks=i+1)).strftime('W%U %Y'))
            
        fig, ax = plt.subplots()

        r_labels = labels[::-1]
        r_closed_issues = closed_issues[::-1]
        r_new_issues = new_issues[::-1]

        ax.bar(r_labels, r_closed_issues, label='closed', color='r', align='edge')
        ax.bar(r_labels, r_new_issues, bottom=r_closed_issues,
               label='new', color='g', align='edge')
        
        ax.legend()
       
