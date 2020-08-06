import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { SseService, Message } from 'src/app/sse.service';
import { Observable } from 'rxjs';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-view-panel',
  templateUrl: './view-panel.component.html',
  styleUrls: ['./view-panel.component.scss'],
})
export class ViewPanelComponent implements OnInit {
  constructor(
    private sseService: SseService,
    private cd: ChangeDetectorRef,
    private sanitizer: DomSanitizer
  ) {}

  observable: Observable<number>;
  messages: any[];

  ngOnInit(): void {
    this.messages = null;
    // this.sseService
    //   .getServerSentEvent(
    //     'http://localhost:8000/api/manhuaren/chapter/manhua-dr-stone?idx=1&m_type_int=2'
    //   )
    //   .subscribe((message) => {
    //     const total = message.total;
    //     if (this.messages === null || this.messages.length !== total) {
    //       this.messages = new Array(total);
    //     }
    //     this.messages[message.idx] = this.sanitizer.bypassSecurityTrustUrl(
    //       'data:image/jpeg;base64,' + message.message
    //     );

    //     this.cd.detectChanges();
    //   });
  }
}
