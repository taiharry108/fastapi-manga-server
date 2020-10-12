import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ApiService } from 'src/app/api.service';
import { convertPySite, MangaSite } from 'src/app/manga-site.enum';
import { Manga, MangaSimple } from 'src/app/model/manga';

@Component({
  selector: 'app-favorite',
  templateUrl: './favorite.component.html',
  styleUrls: ['./favorite.component.scss'],
})
export class FavoriteComponent implements OnInit {
  ngUnsubscribe = new Subject<void>();

  mangas: Manga[];
  mediaServerUrl: string;
  constructor(private api: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.api.getFavs();
    this.mediaServerUrl = this.api.mediaServerUrl;
    this.api.favMangas
      .pipe(takeUntil(this.ngUnsubscribe))
      .subscribe((mangas) => {
        this.mangas = mangas.map((manga) => {
          return { ...manga, isFav: true };
        });
      });
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  onCardClicked(manga: Manga) {
    const site = convertPySite(manga.site);
    this.api.currentSite = site;
    this.api.getIndexPage(manga.id);
    this.router.navigate(['/manga-index']);
  }

  onFavIconClicked(ms: MangaSimple) {    
    this.api.delFav(ms.id);
  }
}
