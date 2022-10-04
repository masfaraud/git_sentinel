import { Component } from '@angular/core';
import { AdminService } from './services/admin.service';
import { MegaMenuItem, MenuItem } from 'primeng/api';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'git project management';
  items: MegaMenuItem[];
  updating: boolean = false;
  last_update_failed:boolean = false;

  constructor(
    private adminService: AdminService
  ) { }

  ngOnInit() {

    this.items = [
                {label: 'Repositories', icon: 'pi pi-fw pi-clone',
                 routerLink: '/repositories'},
                {label: 'Issues', icon: 'pi pi-ticket', routerLink: '/issues'},
                {label: 'Branches', icon: 'pi pi-sort-alt', routerLink: '/branches'},
                {label: 'Pull requests', icon: 'pi pi-reply', routerLink: '/pull-requests'},
                {label: 'Milestones', icon: 'pi pi-tag', routerLink: '/milestones'},
                {label: 'Developers', icon: 'pi pi-user', routerLink: '/developers'},
                {label: 'Platforms', icon: 'pi pi-sitemap', routerLink: '/platforms'},

            ]
      }

  update(){
    this.updating = true;
    this.last_update_failed = false;
    this.adminService.update().subscribe(
      (res) => {
        this.updating = false;
      },
      (error) => {
        this.last_update_failed = true;
        this.updating = false;      }
    );

  }
}
