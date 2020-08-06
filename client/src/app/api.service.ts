import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { SearchResult } from './model/search-result';
import { Subject } from 'rxjs';
import { Manga } from './model/manga';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  serverUrl = environment.serverUrl;
  constructor(private http: HttpClient) {}

  searchResultSubject = new Subject<SearchResult[]>();
  mangaWIthIndexResultSubject = new Subject<Manga>();
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
}
