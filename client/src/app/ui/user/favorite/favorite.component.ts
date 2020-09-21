import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ApiService } from 'src/app/api.service';
import { convertPySite, MangaSite } from 'src/app/manga-site.enum';
import { Manga } from 'src/app/model/manga';

@Component({
  selector: 'app-favorite',
  templateUrl: './favorite.component.html',
  styleUrls: ['./favorite.component.scss'],
})
export class FavoriteComponent implements OnInit {
  ngUnsubscribe = new Subject<void>();

  mangas$: Observable<Manga[]>;
  mediaServerUrl: string;

  constructor(private api: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.api.getFavs();
    this.mediaServerUrl = this.api.mediaServerUrl;
    console.log(this.mediaServerUrl);
    this.mangas$ = this.api.favMangas;
    this.mangas$.subscribe((result) => console.log(result));
  }

  favCardOnClick(manga: Manga) {
    const site = convertPySite(manga.site);
    this.api.currentSite = site;
    const splits = manga.url.split('/');
    const mangaPage = splits[splits.length - 2];
    this.api.getIndexPage(mangaPage);
    this.router.navigate(['/manga-index']);
  }

  onFavIconClicked(mangaId: number): void {
    this.api.delFav(mangaId);    
  }
}
