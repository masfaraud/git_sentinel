#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3
"""

"""
import ciso8601
import pony.orm
import requests

gitea_token = '136035a957c3587045fc1ea3bb6ea1f87a2270ed'
github_token = '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'


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
        # print(req.text, req.url)
        for req_issue in req.json():
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
    
    @pony.orm.db_session()
    def get_issues(self):
        for repo in self.repositories:
            repo.get_issues()
                
class Repository(pony_db.Entity):
    name = pony.orm.Required(str, 255)
    issues = pony.orm.Set('Issue')
    active = pony.orm.Required(bool, default=False)

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
            if not issue:
                created_at = int(ciso8601.parse_datetime(req_issue['created_at']).timestamp())
                updated_at = int(ciso8601.parse_datetime(req_issue['updated_at']).timestamp())
                print('state', req_issue['state'])
                closed = req_issue['state']=='closed'
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
    def update(self):
        for platform in GitPlatform.select():
            platform.get_repos()
        for repo in Repository.select(lambda r:r.active):
            repo.get_issues()
    
    @pony.orm.db_session()
    def plot_issues(self, months=12):
        # start_ts = time.time() - 12*31*24*3600
        for issue in Issue.select():
            print(issue.closed, issue.title)
        
# class Milestone(pony_db.Entity):
    
#     issues = pony.orm.Set(Issue)
    