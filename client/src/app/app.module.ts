import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ViewPanelComponent } from './ui/view-panel/view-panel.component';
import { SearchFormComponent } from './ui/search-form/search-form.component';
import { ClickOutsideDirective } from './common/click-outside.directive';
import { MangaIndexComponent } from './ui/manga-index/manga-index.component';

@NgModule({
  declarations: [
    AppComponent,
    ViewPanelComponent,
    SearchFormComponent,
    ClickOutsideDirective,
    MangaIndexComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
