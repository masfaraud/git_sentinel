import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";

import { IssuesService } from "../../services/issues.service";
import { Issue } from "../../models";

@Component({
  selector: 'app-issue',
  templateUrl: './issue.component.html',
  styleUrls: ['./issue.component.css']
})
export class IssueComponent implements OnInit {

  issue: Issue;
  issue_id: number;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private issuesService: IssuesService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe((params) => (this.issue_id = params.id));
    this.getIssue()
  }

  getIssue(){
    this.issuesService.getIssue(this.issue_id)
    .subscribe(
      (res) => {
        this.issue = res;
      },
      (error) => {
      }
    );
  }

}
