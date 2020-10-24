import { Component, OnInit, OnDestroy } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { Observable, Subject } from 'rxjs';
import { Manga } from 'src/app/model/manga';
import { MangaIndexType } from 'src/app/model/manga-index-type.enum';
import { takeUntil } from 'rxjs/operators';
import { Chapter } from 'src/app/model/chapter';

declare var $: any;

@Component({
  selector: 'app-manga-index',
  templateUrl: './manga-index.component.html',
  styleUrls: ['./manga-index.component.scss'],
})
export class MangaIndexComponent implements OnInit, OnDestroy {
  manga$: Observable<Manga>;
  ngUnsubscribe = new Subject<void>();
  activatedTab: number;
  MangaIndexType = MangaIndexType;
  lastReadChapter$: Observable<Chapter>;
  mediaServerUrl: string;

  constructor(private api: ApiService) {
    this.manga$ = this.api.mangaWIthIndexResultSubject;
    this.lastReadChapter$ = this.api.lastReadChapter;
  }

  ngOnInit(): void {
    this.activatedTab = 0;
    this.api.getFavs();
    this.manga$.pipe(takeUntil(this.ngUnsubscribe)).subscribe((manga) => {
      this.api.addHistory(manga.id);
      this.api.getLastRead(manga.id);
    });
    this.mediaServerUrl = this.api.mediaServerUrl;
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  onLinkClicked(pageUrl: string, mangaId: number) {
    $('#exampleModalCenter').modal('show');
    this.api.getImages(mangaId, pageUrl);
    this.api.updateLastRead(mangaId, pageUrl);
  }

  onTabLinkClicked(idx: number) {
    this.activatedTab = idx;
  }

  get tabNames(): string[] {
    const keys = Object.keys(MangaIndexType);
    return keys.slice(keys.length / 2, keys.length);
  }

  isFav(mangaId: number): boolean {
    return this.favMangaIds !== undefined && this.favMangaIds.includes(mangaId);
  }

  get favMangaIds(): number[] {
    return this.api.favMangaIds;
  }

  onFavIconClicked(mangaId: number): void {
    if (this.isFav(mangaId)) this.api.delFav(mangaId);
    else this.api.addFav(mangaId);
  }
}
