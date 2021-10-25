import { Observable } from 'rxjs';
import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Repository } from '../models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RepositoriesService {

  private repos_url: string = environment.api_url+"/repositories";

  constructor(
    private http: HttpClient,
  ) { }

  getRepos(): Observable<Repository[]> {
    return this.http.get<Repository[]>(this.repos_url);
  }

}
