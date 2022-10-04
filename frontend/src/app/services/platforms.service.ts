import { Observable } from 'rxjs';
import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Platform } from '../models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PlatformsService {
  private platforms_url: string = environment.api_url+"/platforms";

  constructor(
    private http: HttpClient,
  ) { }

  getPlatforms(): Observable<Platform[]> {
    return this.http.get<Platform[]>(this.platforms_url);
  }

  getPlatform(platform_id): Observable<Platform> {
    return this.http.get<Platform>(this.platforms_url+'/'+platform_id);
  }


}
