import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { IssuesStats } from "../../models";

@Component({
  selector: 'app-issues-stats',
  templateUrl: './issues-stats.component.html',
  styleUrls: ['./issues-stats.component.css']
})
export class IssuesStatsComponent implements OnInit , OnChanges{
  @Input() issues_stats: IssuesStats;
  percent_cat: number = 15;
  percent_prio: number= 10;
  percent_cat_prio: number= 20;
  value: number= 0.23;
  constructor() { }

  ngOnInit(): void {
    console.log(this.percent_cat)
    this.percent_cat = 17;
    // this.value = 76;
    console.log('value', this.value)
  }

  ngOnChanges(): void {
    console.log(this.percent_cat)
    this.percent_cat = Math.floor(100 - 100 * this.issues_stats.number_issues_uncategorized/this.issues_stats.number_open_issues);
    this.percent_prio = 100 - 100 * this.issues_stats.number_issues_unprioritized/this.issues_stats.number_open_issues;
    this.percent_cat_prio = 100 - 100 * this.issues_stats.number_issues_unprioritized_uncategorized/this.issues_stats.number_open_issues;
    console.log(this.percent_cat)
  }

}
