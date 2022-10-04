import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";

import { PlatformsService } from "../../services/platforms.service";
import { Platform } from "../../models";

@Component({
  selector: 'app-platform-details',
  templateUrl: './platform-details.component.html',
  styleUrls: ['./platform-details.component.css']
})
export class PlatformDetailsComponent implements OnInit {
  platform: Platform;
  platform_id: number;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private platformsService: PlatformsService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe((params) => (this.platform_id = params.id));
    this.getPlatform()
  }

  getPlatform(){
    this.platformsService.getPlatform(this.platform_id)
    .subscribe(
      (res) => {
        this.platform = res;
      },
      (error) => {
      }
    );
  }
}
