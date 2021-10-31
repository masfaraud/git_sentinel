import { Component, OnInit } from '@angular/core';
import { DevelopersService } from "../services/developers.service";
import { Developer } from "../models";

@Component({
  selector: 'app-developers',
  templateUrl: './developers.component.html',
  styleUrls: ['./developers.component.css']
})
export class DevelopersComponent implements OnInit {

  developers: Developer[];

  constructor(
      private developersService: DevelopersService,
  ) { }

  ngOnInit(): void {
    this.getDevelopers();
  }

  getDevelopers() {
  this.developersService
    .getDevelopers()
    .subscribe(
      (res) => {
        this.developers = res['developers'];
      },
      (error) => {
      }
    );
  }

}
