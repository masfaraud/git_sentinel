import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { RepositoriesComponent } from './repositories/repositories.component';
import { IssuesComponent } from './issues/issues.component';
import { MilestonesComponent } from './milestones/milestones.component';
import { RepositoryComponent } from './repositories/repository/repository.component';
import { IssueComponent } from './issues/issue/issue.component';
import { MilestoneComponent } from './milestones/milestone/milestone.component';
import { DevelopersComponent } from './developers/developers.component';
import { DeveloperComponent } from './developers/developer/developer.component';
import { IssuesTableComponent } from './issues/issues-table/issues-table.component';
import { PullRequestsComponent } from './pull-requests/pull-requests.component';
import { PullRequestComponent } from './pull-requests/pull-request/pull-request.component';

import { NgPipesModule } from "ngx-pipes";

import { NuMarkdownModule } from '@ng-util/markdown';

// PrimeNG
import { CardModule } from 'primeng/card';
import { MegaMenuModule } from 'primeng/megamenu';
import { TableModule } from 'primeng/table';
import {ProgressSpinnerModule} from 'primeng/progressspinner';
import { TagModule } from 'primeng/tag';

@NgModule({
  declarations: [
    AppComponent,
    RepositoriesComponent,
    RepositoryComponent,
    IssuesComponent,
    MilestonesComponent,
    IssueComponent,
    MilestoneComponent,
    DevelopersComponent,
    DeveloperComponent,
    IssuesTableComponent,
    PullRequestsComponent,
    PullRequestComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    CardModule,
    TagModule,
    MegaMenuModule,
    TableModule,
    ProgressSpinnerModule,
    NgPipesModule,
    NuMarkdownModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
