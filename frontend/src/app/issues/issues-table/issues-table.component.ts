import { Component, OnInit, Input } from '@angular/core';
import { Issue } from "../../models";

@Component({
  selector: 'app-issues-table',
  templateUrl: './issues-table.component.html',
  styleUrls: ['./issues-table.component.css']
})
export class IssuesTableComponent implements OnInit {
  @Input() issues: Issue[];

  constructor() { }

  ngOnInit(): void {
  }

}
