import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { SearchResult } from './model/search-result';
import { Subject } from 'rxjs';
import { Manga } from './model/manga';
import { MangaIndexType } from './model/manga-index-type.enum';
import { SseService, Message } from './sse.service';
import { MangaSite } from './manga-site.enum';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient, private sseService: SseService) {
    this._currentSite = MangaSite.ManHuaRen;
  }
  serverUrl = environment.serverUrl;
  _currentSite: MangaSite;

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

  get allSiteNames(): string[] {
    const keys = Object.keys(MangaSite);
    return keys.map(key => MangaSite[key]);
  }

  set currentSite(siteVal: MangaSite) {
    this._currentSite = siteVal;
  }

  get currentSite(): MangaSite {
    return this._currentSite;
  }

  get site(): string {
    switch(this.currentSite) {
      case MangaSite.ManHuaRen:
        return "manhuaren";
      case MangaSite.ManHuaDB:
        return "manhuadb"
      case MangaSite.ManHuaGui:
        return "manhuagui"
      default:
        return "manhuaren";
    }
  }

  searchManga(keyword: string) {
    const url = `${this.serverUrl}search/${this.site}/${keyword}`;

    this.http.get<SearchResult[]>(url).subscribe((result) => {
      this._searchEmpty = false;
      this.searchResultSubject.next(result);
    });
  }

  getIndexPage(mangaPage: string) {
    const url = `${this.serverUrl}index/${this.site}/${mangaPage}`;
    this.http.get<Manga>(url).subscribe((result) => {
      this.mangaWIthIndexResultSubject.next(result);
    });
  }

  getImages(mangaUrl: string, mType: MangaIndexType, idx: number) {
    const splits = mangaUrl.split('/');
    const mangaPage = splits[splits.length - 2];    
    const url = `${this.serverUrl}chapter/${this.site}/${mangaPage}?idx=${idx}&m_type_int=${mType}`;
    console.log(url);
    this.sseService.getServerSentEvent(url).subscribe((message) => {
      this.imagesSseEvent.next(message);
    });
  }
}
