import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { SearchResult } from './model/search-result';
import { Subject, Observable } from 'rxjs';
import { Manga } from './model/manga';
import { MangaIndexType } from './model/manga-index-type.enum';
import { SseService, Message } from './sse.service';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  serverUrl = environment.serverUrl;
  constructor(private http: HttpClient, private sseService: SseService) {}

  searchResultSubject = new Subject<SearchResult[]>();
  mangaWIthIndexResultSubject = new Subject<Manga>();

  imagesSseEvent = new Subject<Message>();

  private _searchEmpty = true;

  emptySearch() {
    this._searchEmpty = true;
    this.searchResultSubject.next(null);
  }

  get searchEmpty(): boolean {
    return this._searchEmpty;
  }

  searchManga(keyword: string) {
    const url = `${this.serverUrl}manhuaren/search/${keyword}`;

    this.http.get<SearchResult[]>(url).subscribe((result) => {
      this._searchEmpty = false;
      this.searchResultSubject.next(result);
    });
  }

  getIndexPage(mangaPage: string) {
    const url = `${this.serverUrl}manhuaren/index/${mangaPage}`;
    this.http.get<Manga>(url).subscribe((result) => {
      this.mangaWIthIndexResultSubject.next(result);
    });
  }

  getImages(mangaPage: string, mType: MangaIndexType, idx: number) {
    const url = `${this.serverUrl}manhuaren/chapter/${mangaPage}?idx=${idx}&m_type_int=${mType}`;
    this.sseService.getServerSentEvent(url).subscribe((message) => {
      this.imagesSseEvent.next(message);
    });
  }
}
