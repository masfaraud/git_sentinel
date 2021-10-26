import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RepositoriesComponent } from './repositories/repositories.component'
import { RepositoryComponent } from './repositories/repository/repository.component';
import { IssuesComponent } from './issues/issues.component'
import { MilestonesComponent } from './milestones/milestones.component'

const routes: Routes = [
  { path: 'repositories', component: RepositoriesComponent },
  { path: 'repositories/:id', component: RepositoryComponent },
  { path: 'issues', component: IssuesComponent },
  { path: 'milestones', component: MilestonesComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
