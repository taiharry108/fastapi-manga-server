import { Component, OnInit, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { DomSanitizer } from '@angular/platform-browser';
import { ApiService } from 'src/app/api.service';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-view-panel',
  templateUrl: './view-panel.component.html',
  styleUrls: ['./view-panel.component.scss'],
})
export class ViewPanelComponent implements OnInit, OnDestroy {
  constructor(
    private cd: ChangeDetectorRef,
    private sanitizer: DomSanitizer,
    private api: ApiService
  ) {
    console.log('constructing view panel');
  }
  ngUnsubscribe = new Subject<void>();
  observable: Observable<number>;
  pages: any[];
  mediaServerUrl: string;

  ngOnInit(): void {
    console.log('in view panel init');
    this.pages = null;
    this.mediaServerUrl = this.api.mediaServerUrl;
    this.api.imagesSseEvent
      .pipe(takeUntil(this.ngUnsubscribe))
      .subscribe((page) => {
        const total = page.total;
        if (
          this.pages === null ||
          this.pages.length !== total ||
          this.pages[page.idx] !== undefined
        ) {
          this.pages = new Array(total);
        }
        this.pages[page.idx] = this.sanitizer.bypassSecurityTrustUrl(
          this.mediaServerUrl + page.pic_path
        );

        this.cd.detectChanges();
      });
  }

  ngOnDestroy(): void {
    console.log('in view panel destroy');
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }
}
