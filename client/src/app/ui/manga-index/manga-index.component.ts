import { Component, OnInit, OnDestroy } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { Observable, Subject } from 'rxjs';
import { Manga } from 'src/app/model/manga';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-manga-index',
  templateUrl: './manga-index.component.html',
  styleUrls: ['./manga-index.component.scss'],
})
export class MangaIndexComponent implements OnInit, OnDestroy {
  manga$: Observable<Manga>;
  manga: Manga;
  ngUnsubscribe = new Subject<void>();
  numCol: number;
  numRow: number;
  many: number[];

  constructor(private api: ApiService) {
    this.manga$ = this.api.mangaWIthIndexResultSubject;
      // .pipe(takeUntil(this.ngUnsubscribe))
      // .subscribe((manga) => {
      //   this.manga = manga;
      // });
  }

  ngOnInit(): void {
    this.many = new Array(100);
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }
}
