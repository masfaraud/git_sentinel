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
                {
                    label: 'Repositories', icon: 'pi pi-fw pi-clone',
                    routerLink: '/repositories'
                    // items: [
                    //     [
                    //         {
                    //             label: 'Video 1',
                    //             items: [{label: 'Video 1.1'}, {label: 'Video 1.2'}]
                    //         },
                    //         {
                    //             label: 'Video 2',
                    //             items: [{label: 'Video 2.1'}, {label: 'Video 2.2'}]
                    //         }
                    //     ],
                    //     [
                    //         {
                    //             label: 'Video 3',
                    //             items: [{label: 'Video 3.1'}, {label: 'Video 3.2'}]
                    //         },
                    //         {
                    //             label: 'Video 4',
                    //             items: [{label: 'Video 4.1'}, {label: 'Video 4.2'}]
                    //         }
                    //     ]
                    // ]
                },
                {label: 'Issues', icon: 'pi pi-ticket', routerLink: '/issues'},
                {label: 'Milestones', icon: 'pi pi-tag', routerLink: '/milestones'},

            ]
      }
}
