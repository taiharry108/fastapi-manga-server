import { Component, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ApiService } from 'src/app/api.service';
import { Manga } from 'src/app/model/manga';

@Component({
  selector: 'app-favorite',
  templateUrl: './favorite.component.html',
  styleUrls: ['./favorite.component.scss'],
})
export class FavoriteComponent implements OnInit {
  ngUnsubscribe = new Subject<void>();

  mangas$: Observable<Manga[]>;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getFavs();
    this.mangas$ = this.api.favMangas;
    this.mangas$.subscribe((result) => console.log(result));
      
  }
}
