import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";

import { RepositoriesService } from "../../services/repositories.service";
import { Repository } from "../../models";


@Component({
  selector: 'app-repository',
  templateUrl: './repository.component.html',
  styleUrls: ['./repository.component.css']
})
export class RepositoryComponent implements OnInit {
  repository: Repository;
  repository_id: number;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private repositoriesService: RepositoriesService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe((params) => (this.repository_id = params.id));
    this.getRepository()
  }

  getRepository(){
    this.repositoriesService.getRepository(this.repository_id)
    .subscribe(
      (res) => {
        this.repository = res;
      },
      (error) => {
      }
    );
  }
}
