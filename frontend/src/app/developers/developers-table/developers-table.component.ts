import { Component, OnInit, Input } from '@angular/core';
import { Developer } from 'src/app/models';

@Component({
  selector: 'app-developers-table',
  templateUrl: './developers-table.component.html',
  styleUrls: ['./developers-table.component.css']
})
export class DevelopersTableComponent implements OnInit {
  @Input() developers: Developer[];
  constructor() { }

  ngOnInit(): void {
  }

}
