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

import { NgPipesModule } from "ngx-pipes";

import { NuMarkdownModule } from '@ng-util/markdown';

// PrimeNG
import { CardModule } from 'primeng/card';
import { MegaMenuModule } from 'primeng/megamenu';
import { TableModule } from 'primeng/table';


@NgModule({
  declarations: [
    AppComponent,
    RepositoriesComponent,
    RepositoryComponent,
    IssuesComponent,
    MilestonesComponent,
    IssueComponent,
    MilestoneComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    CardModule,
    MegaMenuModule,
    TableModule,
    NgPipesModule,
    NuMarkdownModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
