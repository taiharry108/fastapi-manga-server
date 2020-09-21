import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-bookmark-icon',
  templateUrl: './bookmark-icon.component.html',
  styleUrls: ['./bookmark-icon.component.scss'],
})
export class BookmarkIconComponent implements OnInit {
  @Input() isFav: boolean;
  @Input() size: number = 2;

  constructor() {}

  ngOnInit(): void {}
}
