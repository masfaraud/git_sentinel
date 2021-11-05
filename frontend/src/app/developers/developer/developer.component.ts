import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";

import { DevelopersService } from "../../services/developers.service";
import { Developer } from "../../models";

@Component({
  selector: 'app-developer',
  templateUrl: './developer.component.html',
  styleUrls: ['./developer.component.css']
})
export class DeveloperComponent implements OnInit {
  developer: Developer;
  developer_id: number;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private developersService: DevelopersService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe((params) => (this.developer_id = params.id));
    this.getDeveloper()

  }

  getDeveloper(){
    this.developersService.getDeveloper(this.developer_id)
    .subscribe(
      (res) => {
        this.developer = res;
      },
      (error) => {
      }
    );
  }


}
