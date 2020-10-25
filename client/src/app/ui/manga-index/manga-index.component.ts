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
  manga: Manga;
  ngUnsubscribe = new Subject<void>();
  activatedTab: number;
  chapIdx: number;
  MangaIndexType = MangaIndexType;
  lastReadChapter$: Observable<Chapter>;
  mediaServerUrl: string;

  constructor(private api: ApiService) {
    this.manga$ = this.api.mangaWIthIndexResultSubject;
    this.lastReadChapter$ = this.api.lastReadChapter;
  }

  ngOnInit(): void {
    this.activatedTab = 0;
    this.chapIdx = null;
    this.api.getFavs();
    this.manga$.pipe(takeUntil(this.ngUnsubscribe)).subscribe((manga) => {
      this.api.addHistory(manga.id);
      this.api.getLastRead(manga.id);
      this.manga = manga;
    });
    this.mediaServerUrl = this.api.mediaServerUrl;
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  private getImages(chapIdx: number) {
    const mangaId = this.manga.id;
    const chapters: Chapter[] = this.manga.chapters[
      MangaIndexType[this.activatedTab]
    ];
    const chapter = chapters[chapIdx];
    const pageUrl = chapter.page_url;
    this.api.getImages(mangaId, pageUrl);
    this.api.updateLastRead(mangaId, pageUrl);
    this.chapIdx = chapIdx;
  }

  onLinkClicked(chapIdx: number) {
    $('#exampleModalCenter').modal('show');
    this.getImages(chapIdx);
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

  onLeftDown() {
    const chapters: Chapter[] = this.manga.chapters[
      MangaIndexType[this.activatedTab]
    ];
    if (this.chapIdx < chapters.length - 1) this.getImages(this.chapIdx + 1);    
    console.log('pressed left');
  }

  onRightDown() {
    const chapters: Chapter[] = this.manga.chapters[
      MangaIndexType[this.activatedTab]
    ];
    if (this.chapIdx > 0) this.getImages(this.chapIdx - 1);    
    console.log('pressed right');
  }
}
