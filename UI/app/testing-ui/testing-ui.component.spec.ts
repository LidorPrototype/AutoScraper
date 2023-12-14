import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestingUiComponent } from './testing-ui.component';

describe('TestingUiComponent', () => {
  let component: TestingUiComponent;
  let fixture: ComponentFixture<TestingUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestingUiComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TestingUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
