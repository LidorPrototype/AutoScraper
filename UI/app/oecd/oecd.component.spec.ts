import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OecdComponent } from './oecd.component';

describe('OecdComponent', () => {
  let component: OecdComponent;
  let fixture: ComponentFixture<OecdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OecdComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OecdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
