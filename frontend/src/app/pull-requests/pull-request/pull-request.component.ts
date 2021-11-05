import { Component, OnInit } from '@angular/core';
import { PullRequestsService } from "../../services/pull-requests.service";
import { PullRequest } from "../../models";
import { ActivatedRoute, Router } from "@angular/router";

@Component({
  selector: 'app-pull-request',
  templateUrl: './pull-request.component.html',
  styleUrls: ['./pull-request.component.css']
})
export class PullRequestComponent implements OnInit {
  pull_request_id: number;
  pull_request: PullRequest;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private pullRequestService: PullRequestsService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe((params) => (this.pull_request_id = params.id));
    this.getPullRequest()
  }

  getPullRequest(){
    this.pullRequestService.getPullRequest(this.pull_request_id)
    .subscribe(
      (res) => {
        this.pull_request = res;
      },
      (error) => {
      }
    );
  }


}
