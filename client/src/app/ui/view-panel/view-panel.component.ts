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
  messages: any[];

  ngOnInit(): void {
    console.log('in view panel init');
    this.messages = null;
    this.api.imagesSseEvent
      .pipe(takeUntil(this.ngUnsubscribe))
      .subscribe((message) => {
        const total = message.total;
        if (
          this.messages === null ||
          this.messages.length !== total ||
          this.messages[message.idx] !== undefined
        ) {
          this.messages = new Array(total);
        }
        this.messages[message.idx] = this.sanitizer.bypassSecurityTrustUrl(
          'data:image/jpeg;base64,' + message.message
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
