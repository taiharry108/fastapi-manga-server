import { Component, OnInit, OnDestroy } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { Observable, Subject } from 'rxjs';
import { Manga } from 'src/app/model/manga';
import { MangaIndexType } from 'src/app/model/manga-index-type.enum';
import { takeUntil } from 'rxjs/operators';

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
  favMangaId: number[];

  constructor(private api: ApiService) {
    this.manga$ = this.api.mangaWIthIndexResultSubject;
  }

  ngOnInit(): void {
    this.activatedTab = 0;
    this.api.getFavs();
    this.api.favMangas
      .pipe(takeUntil(this.ngUnsubscribe))
      .subscribe((mangas) => {
        console.log(mangas)
        this.favMangaId = mangas.map((manga) => manga.id);
        
      });
    this.manga$.pipe(takeUntil(this.ngUnsubscribe)).subscribe((manga) => {
      console.log(manga);
    });
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  onLinkClicked(mangaPage: string, idx: number) {
    $('#exampleModalCenter').modal('show');
    this.api.getImages(mangaPage, this.activatedTab, idx);
  }

  onTabLinkClicked(idx: number) {
    this.activatedTab = idx;
  }

  get tabNames(): string[] {
    const keys = Object.keys(MangaIndexType);
    return keys.slice(keys.length / 2, keys.length);
  }

  isFav(mangaId: number): boolean {
    return this.favMangaId !== undefined && this.favMangaId.includes(mangaId);
  }

  favIconClicked(mangaId: number): void {   
    if (this.isFav(mangaId))
      this.api.delFav(mangaId);
    else
    this.api.addFav(mangaId);
  }
}
