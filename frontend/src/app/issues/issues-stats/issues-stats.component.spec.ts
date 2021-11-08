import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IssuesStatsComponent } from './issues-stats.component';

describe('IssuesStatsComponent', () => {
  let component: IssuesStatsComponent;
  let fixture: ComponentFixture<IssuesStatsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IssuesStatsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IssuesStatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
