import { Component, OnInit } from '@angular/core';
import { IssuesService } from "../services/issues.service";
import { Issue } from "../models";

@Component({
  selector: 'app-issues',
  templateUrl: './issues.component.html',
  styleUrls: ['./issues.component.css']
})
export class IssuesComponent implements OnInit {

  issues: Issue[];
  constructor(
    private issuesService: IssuesService,
  ) { }

  ngOnInit(): void {
    this.getIssues();
  }

  getIssues() {
  this.issuesService
    .getIssues()
    .subscribe(
      (res) => {
        this.issues = res['issues'];
      },
      (error) => {
      }
    );
  }

}
