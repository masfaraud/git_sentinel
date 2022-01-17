import { TestBed } from '@angular/core/testing';

import { MilestonesService } from './milestones.service';

describe('MilestonesService', () => {
  let service: MilestonesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MilestonesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
