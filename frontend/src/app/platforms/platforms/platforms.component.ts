import { Component, OnInit } from '@angular/core';
import { PlatformsService } from "../../services/platforms.service";
import { Platform } from "../../models";


@Component({
  selector: 'app-platforms',
  templateUrl: './platforms.component.html',
  styleUrls: ['./platforms.component.css']
})
export class PlatformsComponent implements OnInit {
  platforms: Platform[];
  constructor(
    private platformService: PlatformsService,
  ) { }


  ngOnInit(): void {
    console.log('init');
    this.getPlatforms();
    console.log(this.platforms);
  }

  getPlatforms() {
  this.platformService
    .getPlatforms()
    .subscribe(
      (res) => {
        this.platforms = res['platforms'];
      },
      (error) => {
      }
    );
  }

}