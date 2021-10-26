import { Injectable } from '@angular/core';
import { Team,User, UserTeamInvitation} from '../models/api';
import { Observable } from 'rxjs/Observable';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { environment } from '../../environments/environment';
import { EngineeringObject } from '../models/api'


@Injectable()
export class ObjectsService {
  private objects_url = `${environment.api_url}/objects`;
  private create_object_url = `${environment.api_url}/objects/create`;
  private objects_classes_url = `${environment.api_url}/objects/classes`;
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient) {}

  getObjectsClasses(): Observable<string[]>{
    return this.http.get<string[]>(this.objects_classes_url)
  }

  getClassHierarchy(): Observable<string[]>{
    return this.http.get<string[]>(this.objects_url+'/class_hierarchy')
  }

  getAllClassObjects(class_name): Observable<EngineeringObject[]>{
    return this.http.get<any[]>(this.objects_url+'/'+String(class_name))
        .map(objs=>{
                var engineering_objects: EngineeringObject[] = [];
                for (let obj of objs){
                  engineering_objects.push(EngineeringObject.deserialize(obj));
                }
                return engineering_objects;
              })
  }

  getClassAttributes(class_name): Observable<any>{
    return this.http.get<any>(this.objects_url+'/'+String(class_name)+'/attributes')
  }

  getClassDefaultDict(class_name): Observable<any>{
    return this.http.get<any>(this.objects_url+'/'+String(class_name)+'/default_dict')
  }

  getObjectDict(class_name, object_id, embedded_subobjects=false): Observable<any>{
    var params = new HttpParams()
                  .set('embedded_subobjects', String(embedded_subobjects));
    return this.http.get<any>(this.objects_url+'/'+String(class_name)+'/'+String(object_id), {params})
  }

  getObject(class_name, object_id, embedded_subobjects=false): Observable<EngineeringObject>{
    return this.getObjectDict(class_name, object_id, embedded_subobjects=embedded_subobjects).map((object_dict)=>{
      return this.instantiateObject(object_dict);})
  }

  getObjectList(class_name, object_ids, embedded_subobjects=false): Observable<EngineeringObject[]>{
    var params = new HttpParams()
                  .set('embedded_subobjects', String(embedded_subobjects))
                  .set('object_ids', String(object_ids));
    return this.http.get<any>(this.objects_url+'/'+String(class_name)+'/object_list', {params})
  }

  getObjectPlotData(class_name, object_id): Observable<any[]>{
    return this.http.get<any>(this.objects_url+'/'+String(class_name)+'/'+String(object_id)+'/plot_data')
  }

  getObjectSTLToken(class_name, object_id): Observable<any[]>{
    return this.http.get<any>(this.objects_url+'/'+String(class_name)+'/'+String(object_id)+'/stl')
  }

  classPrettyName(full_name): string{
    return full_name.split('.').pop()

  }

  defineOrder(properties) {
    let list_sort_default = ['string', 'boolean', 'number', 'object', 'array'];
    let order = [];
    let ordered_temp = {}
    let unordered_temp = {};
    var count = 0;
    for (const [attr, value] of Object.entries(properties)){
      console.log(value, typeof value['order'])
      let conf = {};
      conf[attr] = value;
      if (value.hasOwnProperty('order')) {
        if (value.hasOwnProperty('editable')){
          if (value['editable']){
            ordered_temp[value['order']] = conf;
          }
        }
        if (value['order'] > count){
          count = value['order']
        };
      }
      else{
        if (value.hasOwnProperty('editable')){
          if (value['editable']){
            unordered_temp[attr] = value;
          }
        }
      }
    }

    for (let type of list_sort_default){
      for (const [attr, value] of Object.entries(unordered_temp)){
        if (value["type"] == type){
          // Add non order assigned elements
          let conf = {};
          conf[attr] = value;
          count++;
          ordered_temp[count] = conf;
        }
      }
    }

    for (let i=0; i<Object.keys(properties).length; i++){
      order.push(ordered_temp[i])
    }
  return order
  }

  defineRequired(jsonschema){
    var required_properties = {}
    for (const key of Object.keys(jsonschema['properties'])){
      if (jsonschema['required'].indexOf(key) > -1){
        required_properties[key]=true;
      }
      else
      {
        required_properties[key]=false;
      }
    }
    return required_properties
  }

  createObject(object_class, object_json, embedded_subobjects){
    return this.http
    .post<any>(this.create_object_url, JSON.stringify({object:{class: object_class, json:object_json}, embedded_subobjects : embedded_subobjects}), { headers: this.headers })
    .toPromise()
    .then(object => {return object;})
  }

  replaceObject(object_class, object_id, object_json, embedded_subobjects){
    return this.http
    .post<any>(this.objects_url+'/'+object_class+'/'+object_id+'/replace',
                JSON.stringify({object:{class: object_class, json:object_json}, embedded_subobjects : embedded_subobjects}),
                { headers: this.headers })
    .toPromise()
    .then(object => {return object;})
  }

  updateObject(object_class, object_id, update_dict){
    return this.http
    .post<any>(this.objects_url+'/'+object_class+'/'+object_id+'/update',
              JSON.stringify(update_dict), { headers: this.headers })
    .toPromise()
    .then(object => {return object;})
  }

  deleteObject(object_class, object_id): Observable<any>{
    return this.http
    .delete<any>(this.objects_url+'/'+object_class+'/'+object_id+'/delete',
                {headers: this.headers})
  }

  instantiateObject(object_dict){
    return EngineeringObject.deserialize(object_dict);
  }

  deleteAllSTL(){
    return this.http.delete<any>(this.objects_url+'/stl/delete_all')
  }

}
