import { Observable } from 'rxjs';
import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Milestone } from '../models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MilestonesService {
  private milestones_url: string = environment.api_url+"/milestones";
  constructor(
        private http: HttpClient,
  ) { }


  getMilestones(): Observable<Milestone[]> {
    return this.http.get<Milestone[]>(this.milestones_url);
  }

  getMilestone(milestone_id): Observable<Milestone> {
    return this.http.get<Milestone>(this.milestones_url+'/'+milestone_id);
  }
}
