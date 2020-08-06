import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Message {
  message: string;
  total: number;
  idx: number;
}

@Injectable({
  providedIn: 'root',
})
export class SseService {
  constructor() {}

  getServerSentEvent(url: string): Observable<Message> {
    return Observable.create((observer) => {
      const eventSource = this.getEventSource(url);

      eventSource.onmessage = event => {
        const data = JSON.parse(event.data);
        if (event.data !== "{}")
          { 
            observer.next(data);
          }
        else
          {
            eventSource.close();
          }
      }

      eventSource.onerror = error => {
          observer.error(error);
      }      
    });
  }

  private getEventSource(url: string): EventSource {
    return new EventSource(url);
  }
}
