import { Component, OnInit, OnDestroy } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { Observable, Subject } from 'rxjs';
import { Manga } from 'src/app/model/manga';
import { takeUntil } from 'rxjs/operators';
import { Chapter } from 'src/app/model/chapter';
import { MangaIndexType } from 'src/app/model/manga-index-type.enum';

declare var $: any;

@Component({
  selector: 'app-manga-index',
  templateUrl: './manga-index.component.html',
  styleUrls: ['./manga-index.component.scss'],
})
export class MangaIndexComponent implements OnInit, OnDestroy {
  manga$: Observable<Manga>;
  ngUnsubscribe = new Subject<void>();
  numCol: number;
  numRow: number;
  many: number[];

  constructor(private api: ApiService) {
    this.manga$ = this.api.mangaWIthIndexResultSubject;
  }

  ngOnInit(): void {
    this.many = new Array(100);
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  onLinkClicked(mangaPage: string, idx: number, mType: MangaIndexType) {
    $('#exampleModalCenter').modal('show');    
    this.api.getImages(mangaPage, mType, idx);
  }
}
