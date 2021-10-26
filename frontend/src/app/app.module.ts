import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RepositoriesComponent } from './repositories/repositories.component';

import { CardModule } from 'primeng/card';
import { MegaMenuModule } from 'primeng/megamenu';
import { IssuesComponent } from './issues/issues.component';
import { MilestonesComponent } from './milestones/milestones.component';
import { RepositoryComponent } from './repositories/repository/repository.component';
import { IssueComponent } from './issues/issue/issue.component';

@NgModule({
  declarations: [
    AppComponent,
    RepositoriesComponent,
    RepositoryComponent,
    IssuesComponent,
    MilestonesComponent,
    IssueComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    CardModule,
    MegaMenuModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
