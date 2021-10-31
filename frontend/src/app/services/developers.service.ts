import { Observable } from 'rxjs';
import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Developer } from '../models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DevelopersService {
  private devs_url: string = environment.api_url+"/developers";

  constructor(
    private http: HttpClient,
  ) { }

  getDevelopers(): Observable<Developer[]> {
    return this.http.get<Developer[]>(this.devs_url);
  }

  getDeveloper(dev_id): Observable<Developer> {
    return this.http.get<Developer>(this.devs_url+'/'+dev_id);
  }

}
