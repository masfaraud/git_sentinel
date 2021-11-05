import { Component } from '@angular/core';
import {MegaMenuItem,MenuItem} from 'primeng/api';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'git project management';
  items: MegaMenuItem[];

  ngOnInit() {

    this.items = [
                {label: 'Repositories', icon: 'pi pi-fw pi-clone',
                 routerLink: '/repositories'},
                {label: 'Issues', icon: 'pi pi-ticket', routerLink: '/issues'},
                {label: 'Pull requests', icon: 'pi pi-reply', routerLink: '/pull-requests'},
                {label: 'Milestones', icon: 'pi pi-tag', routerLink: '/milestones'},
                {label: 'Developers', icon: 'pi pi-user', routerLink: '/developers'},

            ]
      }
}
