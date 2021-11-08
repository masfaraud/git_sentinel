import { Observable } from 'rxjs';
import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Issue, IssuesStats } from '../models';
import { environment } from '../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class IssuesService {

  private repos_url: string = environment.api_url+"/issues";

  constructor(
    private http: HttpClient,
  ) { }

  getIssues(): Observable<Issue[]> {
    return this.http.get<Issue[]>(this.repos_url);
  }

  getIssue(issue_id): Observable<Issue> {
    return this.http.get<Issue>(this.repos_url+'/'+issue_id);
  }

  getStats(): Observable<IssuesStats> {
    return this.http.get<IssuesStats>(this.repos_url+'/stats');
  }
}
