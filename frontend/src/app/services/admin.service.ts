import { Observable } from 'rxjs';
import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private admin_url: string = environment.api_url+"/admin";

  constructor(
    private http: HttpClient,
  ) { }

  update(): Observable<boolean> {
    console.log('update!!!');
    console.log(this.admin_url);
    return this.http.get<boolean>(this.admin_url+'/update');
  }
}
