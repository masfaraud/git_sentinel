import { Component, OnInit } from '@angular/core';
import { MilestonesService } from "../services/milestones.service";
import { Milestone } from "../models";

@Component({
  selector: 'app-milestones',
  templateUrl: './milestones.component.html',
  styleUrls: ['./milestones.component.css']
})
export class MilestonesComponent implements OnInit {
  milestones: Milestone[];

  constructor(
    private milestonesService: MilestonesService,
  ) { }

  ngOnInit(): void {
    this.getMilestones()
  }

  getMilestones() {
  this.milestonesService
    .getMilestones()
    .subscribe(
      (res) => {
        console.log(res['milestones'])
        this.milestones = res['milestones'];
      },
      (error) => {
      }
    );
  }

}
