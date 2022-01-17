import { Component, OnInit, Input } from '@angular/core';
import { Milestone } from "../../models";

@Component({
  selector: 'app-milestones-table',
  templateUrl: './milestones-table.component.html',
  styleUrls: ['./milestones-table.component.css']
})
export class MilestonesTableComponent implements OnInit {
  @Input() milestones: Milestone[];
  constructor() { }

  ngOnInit(): void {
  }

}
