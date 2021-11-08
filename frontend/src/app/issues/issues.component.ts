import { Component, OnInit } from '@angular/core';
import { IssuesService } from "../services/issues.service";
import { Issue, IssuesStats } from "../models";

@Component({
  selector: 'app-issues',
  templateUrl: './issues.component.html',
  styleUrls: ['./issues.component.css']
})
export class IssuesComponent implements OnInit {

  issues: Issue[];
  stats: IssuesStats;

  constructor(
    private issuesService: IssuesService,
  ) { }

  ngOnInit(): void {
    // this.stats = [];
    this.getIssues();
    this.getStats();
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

  getStats() {
  this.issuesService
    .getStats()
    .subscribe(
      (res) => {
        this.stats = res['stats'];
      },
      (error) => {
      }
    );
  }


}
