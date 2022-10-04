import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RepositoriesComponent } from './repositories/repositories.component'
import { RepositoryComponent } from './repositories/repository/repository.component';
import { IssuesComponent } from './issues/issues.component'
import { BranchesComponent } from './branches/branches.component'
import { IssueComponent } from './issues/issue/issue.component'
import { MilestonesComponent } from './milestones/milestones.component'
import { MilestoneComponent } from './milestones/milestone/milestone.component'
import { DevelopersComponent } from './developers/developers.component'
import { DeveloperComponent } from './developers/developer/developer.component'
import { PullRequestsComponent } from './pull-requests/pull-requests.component'
import { PullRequestComponent } from './pull-requests/pull-request/pull-request.component'
import { PlatformsComponent } from './platforms/platforms/platforms.component';
import { PlatformDetailsComponent } from './platforms/platform-details/platform-details.component';


const routes: Routes = [
  { path: 'repositories', component: RepositoriesComponent },
  { path: 'repositories/:id', component: RepositoryComponent },
  { path: 'issues', component: IssuesComponent },
  { path: 'issues/:id', component: IssueComponent },
  { path: 'milestones', component: MilestonesComponent },
  { path: 'milestones/:id', component: MilestoneComponent },
  { path: 'developers', component: DevelopersComponent },
  { path: 'developers/:id', component: DeveloperComponent },
  { path: 'pull-requests', component: PullRequestsComponent },
  { path: 'pull-requests/:id', component: PullRequestComponent },
  { path: 'branches', component: BranchesComponent },
  { path: 'platforms', component: PlatformsComponent },
  { path: 'platforms/:id', component: PlatformDetailsComponent },

];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
