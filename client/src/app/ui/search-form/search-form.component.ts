import { Component, OnInit, OnDestroy } from '@angular/core';
import {
  FormGroup,
  FormBuilder,
  FormControl,
  Validators,
} from '@angular/forms';
import { ApiService } from 'src/app/api.service';
import { SearchResult } from 'src/app/model/search-result';
import { Observable, Subject } from 'rxjs';
import { takeUntil, debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { Router } from '@angular/router';

declare var $: any;

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss'],
})
export class SearchFormComponent implements OnInit, OnDestroy {
  form: FormGroup;
  search = new FormControl('', Validators.required);
  site = new FormControl();
  searchResult: Observable<SearchResult[]>;
  ngUnsubscribe = new Subject<void>();
  private _dropdownHidden: boolean;

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private router: Router
  ) {
    this.form = this.fb.group({
      search: this.search,
      site: this.site,
    });
    this.searchResult = this.api.searchResultSubject;
    this.form.controls.site.setValue(this.api.currentSite);
  }

  ngOnInit(): void {
    this._dropdownHidden = true;
    this.form.valueChanges
      .pipe(takeUntil(this.ngUnsubscribe))
      .pipe(debounceTime(150), distinctUntilChanged())
      .subscribe((value) => {
        const { search, site } = value;
        console.log(site);
        this.api.currentSite = site;
        if (search.length > 3) this.api.searchManga(search);
        if (search.length === 0) this.api.emptySearch();
      });
  }

  suggestionOnClick(mangaId: number) {
    this.api.getIndexPage(mangaId);
    this.router.navigate(['/manga-index']);
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  onClick() {
    const { search } = this.form.value;
    this.api.searchManga(search);
  }

  get dropdownHidden(): boolean {
    return this._dropdownHidden || this.api.searchEmpty;
  }

  onClickOutside() {
    this._dropdownHidden = true;
  }

  onDivClick() {
    this._dropdownHidden = false;
  }

  get siteNames(): string[] {
    return this.api.allSiteNames;
  }
}
