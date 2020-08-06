import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MangaIndexComponent } from './manga-index.component';

describe('MangaIndexComponent', () => {
  let component: MangaIndexComponent;
  let fixture: ComponentFixture<MangaIndexComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MangaIndexComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MangaIndexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
