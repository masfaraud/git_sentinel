import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MilestonesTableComponent } from './milestones-table.component';

describe('MilestonesTableComponent', () => {
  let component: MilestonesTableComponent;
  let fixture: ComponentFixture<MilestonesTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MilestonesTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MilestonesTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
