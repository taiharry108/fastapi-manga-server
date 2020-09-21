import { Component, OnInit, ChangeDetectionStrategy, Input, Output, EventEmitter } from '@angular/core';
import { Manga } from 'src/app/model/manga';

@Component({
  selector: 'app-manga-list',
  templateUrl: './manga-list.component.html',
  styleUrls: ['./manga-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MangaListComponent implements OnInit {
  @Input() title: string;
  @Input() mangas: Manga[];
  @Input() mediaServerUrl: string;
  @Output() favIconClicked = new EventEmitter<number>();
  @Output() cardClicked = new EventEmitter<Manga>();

  constructor() {}

  ngOnInit(): void {}

  onFavIconClicked(mangaId: number): void {
    this.favIconClicked.emit(mangaId);
  }

  onCardClicked(manga: Manga) {
    this.cardClicked.emit(manga);
  }  
}
