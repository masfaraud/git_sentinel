import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DevelopersTableComponent } from './developers-table.component';

describe('DevelopersTableComponent', () => {
  let component: DevelopersTableComponent;
  let fixture: ComponentFixture<DevelopersTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DevelopersTableComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DevelopersTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
