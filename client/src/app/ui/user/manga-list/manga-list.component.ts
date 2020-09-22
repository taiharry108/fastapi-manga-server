import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  Input,
  Output,
  EventEmitter,
} from '@angular/core';
import { Manga, MangaSimple } from 'src/app/model/manga';

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
  @Output() favIconClicked = new EventEmitter<MangaSimple>();
  @Output() cardClicked = new EventEmitter<Manga>();

  constructor() {}

  ngOnInit(): void {}

  onFavIconClicked(mangaId: number, isFav: boolean): void {
    const ms: MangaSimple = {
      id: mangaId,
      isFav: isFav,
    };
    this.favIconClicked.emit(ms);
  }

  onCardClicked(manga: Manga) {
    this.cardClicked.emit(manga);
  }
}
