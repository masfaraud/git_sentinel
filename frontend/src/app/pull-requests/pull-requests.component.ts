import { Component, OnInit } from '@angular/core';
import { PullRequestsService } from "../services/pull-requests.service";
import { PullRequest } from "../models";

@Component({
  selector: 'app-pull-requests',
  templateUrl: './pull-requests.component.html',
  styleUrls: ['./pull-requests.component.css']
})
export class PullRequestsComponent implements OnInit {

  pull_requests: PullRequest[];

  constructor(
        private pullRequestsService: PullRequestsService,
  ) { }

  ngOnInit(): void {
    this.getPullRequests()
  }

  getPullRequests() {
  this.pullRequestsService
    .getPullRequests()
    .subscribe(
      (res) => {
        this.pull_requests = res['pull_requests'];
      },
      (error) => {
      }
    );
  }


}
