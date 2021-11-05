import { Observable } from 'rxjs';
import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { PullRequest } from '../models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PullRequestsService {
  private pull_requests_url: string = environment.api_url+"/pull-requests";

  constructor(
    private http: HttpClient,
  ) { }

  getPullRequests(): Observable<PullRequest[]> {
    return this.http.get<PullRequest[]>(this.pull_requests_url);
  }

  getPullRequest(pull_request_id): Observable<PullRequest> {
    return this.http.get<PullRequest>(this.pull_requests_url+'/'+pull_request_id);
  }


}
