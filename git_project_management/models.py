#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3
"""

"""
import time
import datetime
import ciso8601
import pony.orm
import requests
import statistics
import matplotlib.pyplot as plt

STALL_PR_WARNING_TIME = 2*24*3600

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

    def plot_milestones(self):
        for milestone in self.milestones.select(lambda m:not m.closed_at).order_by(Milestone.due_on):
            print(milestone.title)
            print(milestone.due_on, milestone.closed_at)
            closed_issues = milestone.issues.select(lambda i:i.closed).count()
            open_issues = milestone.issues.select(lambda i:not i.closed).count()
            print('progress ', closed_issues/(closed_issues + open_issues)*100, '%')

    def stalled_branches(self):
        pass

    @pony.orm.db_session()
    def issue_types(self):
        return list(set([i.type for i in self.issues.select(lambda j:len(j.type)>0)]))
    
    def issue_priorities(self):
        return list(set([i.priority for i in self.issues.select(lambda j:len(j.priority)>0)]))
    

    @pony.orm.db_session()
    def plot_issues(self, weeks=15):
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=True)

        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()


        labels = []
        open_issues = []
        new_issues = []
        closed_issues = []
        no_milestone_issues = []
        mean_closing_time = []
        max_closing_time = []
        # std_closing_time_week = []

        issues_by_types = {t: [] for t in self.issue_types()}
        issues_by_types['uncategorized'] = []
        
        issues_by_priority = {p: [] for p in self.issue_priorities()}
        issues_by_priority['unprioritized'] = []

        now = datetime.datetime.now()
        for iw in range(weeks):
            week_start = (now - datetime.timedelta(weeks=iw+1)).timestamp()
            week_end = (now - datetime.timedelta(weeks=iw)).timestamp()
            
            open_issues_week = self.issues.select(lambda i:i.created_at<week_end and (not i.closed or i.closed_at>week_end))
            new_issues_week = self.issues.select(lambda i:i.created_at>week_start and i.created_at<week_end)
            closed_issues_week = self.issues.select(lambda i:i.closed_at<week_end and i.closed_at>week_start)
            
            number_closed_issues_week = closed_issues_week.count()
            close_times = [(i.closed_at - i.created_at)/3600/24 for i in closed_issues_week]
            # print(close_times)
            if number_closed_issues_week:
                
                mean_closing_time_week = statistics.mean(close_times)
                max_closing_time_week = max(close_times)
                # print(mean_closing_time_week, std_closing_time_week)
            else:
                mean_closing_time_week = 0.
                max_closing_time_week = 0.
                
            mean_closing_time.append(mean_closing_time_week)
            max_closing_time.append(max_closing_time_week)
            
            
            
            no_milestone_issues_week = [i for i in open_issues_week if not i.milestone]
            
            open_issues.append(open_issues_week.count())
            new_issues.append(new_issues_week.count())
            closed_issues.append(number_closed_issues_week)
            no_milestone_issues.append(len(no_milestone_issues_week))
            labels.append((now - datetime.timedelta(weeks=iw+1)).strftime('W%U %Y'))
            
            for v in issues_by_types.values():
                v.append(0)
            for v in issues_by_priority.values():
                v.append(0)
            
            for issue in open_issues_week:
                if issue.type:
                    issues_by_types[issue.type][-1] += 1
                else:
                    issues_by_types['uncategorized'][-1] += 1
                    
                if issue.priority:
                    issues_by_priority[issue.priority][-1] += 1
                else:
                    issues_by_priority['unprioritized'][-1] += 1
                

        r_labels = labels[::-1]
        
        r_closed_issues = closed_issues[::-1]
        r_new_issues = new_issues[::-1]
        r_open_issues = open_issues[::-1]
        r_no_milestone_issues = no_milestone_issues[::-1]
        r_max_closing_time = max_closing_time[::-1]
        r_mean_closing_time = mean_closing_time[::-1]

        ax1.bar(r_labels, r_closed_issues, label='closed in the week', color='r', align='edge')
        ax1.bar(r_labels, r_new_issues, bottom=r_closed_issues,
               label='new in the week', color='g', align='edge')
        # print(str(self))
        ax1.legend()

        current_bottom = [0]*len(labels)
        for type_, issue_number in issues_by_types.items():
            color = Issue.type_color(type_)
            ax2.bar(r_labels, issue_number[::-1], bottom=current_bottom,
                    color=color, label='type: '+type_, align='edge')
            current_bottom = issue_number[::-1]
        ax2.legend()

        current_bottom = [0]*len(labels)
        for priority, issue_number in issues_by_priority.items():
            color = Issue.priority_color(priority)
            ax3.bar(r_labels, issue_number[::-1], bottom=current_bottom,
                    color=color, label=priority, align='edge')
            current_bottom = issue_number[::-1]
        ax3.legend()
        
        ax4.bar(r_labels, r_no_milestone_issues, label='No milestones issues',
                color='y', align='edge')
        ax4.legend()
        
        ax5.bar(r_labels, r_max_closing_time,
               label='Max closing time (days)', color='r', align='edge')
        ax5.bar(r_labels, r_mean_closing_time, color='b', label='Mean closing time (days)', align='edge')

        ax5.legend()
        
        ax1.set_title(str(self))

class GiteaRepository(Repository):
    platform = pony.orm.Required(GiteaPlatform)
    owner = pony.orm.Required(str, 100)
    
    @pony.orm.db_session()
    def get_issues(self):
        page_number_issues = 1
        page_number = 1
        while page_number_issues:
            # print('page', page_number)
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
    
                if req_issue['labels']:
                    for label in req_issue['labels']:
                        for label_prefix in ['priority', 'type']:
                            full_prefix = label_prefix + ':'
                            if label['name'].startswith(full_prefix):
                                value = label['name'].replace(full_prefix, '')
                                value = value.lstrip(' ').lower()
                                if value:
                                    setattr(issue, label_prefix, value)

    
                if req_issue['milestone']:
                    # print(req_issue['milestone'])
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
            merged = req_pr['merged']
            mergeable = req_pr['mergeable']
            
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
                pull_request.mergeable = mergeable   
    
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
    type = pony.orm.Optional(str)
    priority = pony.orm.Optional(str)
    
    @staticmethod
    def type_color(type_):
        colors = {'bug': 'r', 'uncategorized': 'grey'}
        if type_ in colors:
            return colors[type_]
        else:
            return None

    @staticmethod
    def priority_color(priority):
        colors = {'critical': 'darkred',
                  'high': 'r',
                  'medium': 'y',
                  'low': 'blue',
                  'unprioritized': 'grey'}
        if priority in colors:
            return colors[priority]
        else:
            return None
    
    @classmethod
    def get_all_types(cls):
        return list(set([i.type for i in cls.select(lambda j:j.type)]))
    
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
    
    @classmethod
    def mergeable_pull_requests(cls):
        return cls.select(lambda pr: pr.mergeable and (not pr.merged))
    
    @classmethod
    def stalled_pull_requests(cls):
        return cls.select(lambda pr: pr.mergeable and (not pr.merged) and pr.updated_at - time.time()>STALL_PR_WARNING_TIME)
    
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
       
