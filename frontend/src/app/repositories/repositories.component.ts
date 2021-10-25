import { Component, OnInit } from '@angular/core';
import { RepositoriesService } from "../services/repositories.service";
import { Repository } from "../models";

@Component({
  selector: 'app-repositories',
  templateUrl: './repositories.component.html',
  styleUrls: ['./repositories.component.css']
})
export class RepositoriesComponent implements OnInit {
  repositories: Repository[];
  constructor(
    private repositoriesService: RepositoriesService,
  ) { }

  ngOnInit(): void {
    console.log('init');
    this.getRepos();
    console.log(this.repositories);
  }

  getRepos() {
  this.repositoriesService
    .getRepos()
    .subscribe(
      (res) => {
        this.repositories = res['repositories'];
      },
      (error) => {
      }
    );
  }

}
