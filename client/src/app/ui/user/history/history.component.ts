import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ApiService } from 'src/app/api.service';
import { convertPySite } from 'src/app/manga-site.enum';
import { Manga } from 'src/app/model/manga';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss'],
})
export class HistoryComponent implements OnInit, OnDestroy {
  ngUnsubscribe = new Subject<void>();

  mangas: Manga[];
  mediaServerUrl: string;
  constructor(private api: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.api.getHistory();
    this.mediaServerUrl = this.api.mediaServerUrl;
    this.api.historyMangas
      .pipe(takeUntil(this.ngUnsubscribe))
      .subscribe((mangas) => (this.mangas = mangas));
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  onCardClicked(manga: Manga) {
    const site = convertPySite(manga.site);
    this.api.currentSite = site;
    const splits = manga.url.split('/');
    const mangaPage = splits[splits.length - 2];
    this.api.getIndexPage(mangaPage);
    this.router.navigate(['/manga-index']);
  }

  onFavIconClicked(mangaId: number) {
    this.api.delFav(mangaId);
  }
}
