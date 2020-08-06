import { Component, OnInit } from '@angular/core';
import { SearchResult } from 'src/app/model/search-result';
import { Observable } from 'rxjs';
import { ApiService } from 'src/app/api.service';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit {
  searchResult: Observable<SearchResult[]>;
  constructor(private api: ApiService) { 
    this.searchResult = this.api.searchResultSubject;
  }

  ngOnInit(): void {    
  }

}
