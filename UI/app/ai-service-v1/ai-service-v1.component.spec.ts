import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AiServiceV1Component } from './ai-service-v1.component';

describe('AiServiceV1Component', () => {
  let component: AiServiceV1Component;
  let fixture: ComponentFixture<AiServiceV1Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AiServiceV1Component ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AiServiceV1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
