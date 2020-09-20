import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ViewPanelComponent } from './ui/view-panel/view-panel.component';
import { SearchFormComponent } from './ui/search-form/search-form.component';
import { ClickOutsideDirective } from './common/click-outside.directive';
import { MangaIndexComponent } from './ui/manga-index/manga-index.component';
import { MainComponent } from './ui/main/main.component';
import { GoogleAuthComponent } from './ui/auth/google-auth/google-auth.component';
import { HttpRequestInterceptor } from './common/http-request-interceptor';
import { UserNavComponent } from './ui/auth/user-nav/user-nav.component';
import { ProfileComponent } from './ui/user/profile/profile.component';
import { HistoryComponent } from './ui/user/history/history.component';
import { FavoriteComponent } from './ui/user/favorite/favorite.component';
import { BookmarkIconComponent } from './ui/common/bookmark-icon/bookmark-icon.component';
import { MangaSitePipe } from './model/manga-site.pipe';

@NgModule({
  declarations: [
    AppComponent,
    ViewPanelComponent,
    SearchFormComponent,
    ClickOutsideDirective,
    MangaIndexComponent,
    MainComponent,
    GoogleAuthComponent,
    UserNavComponent,
    ProfileComponent,
    HistoryComponent,
    FavoriteComponent,
    BookmarkIconComponent,
    MangaSitePipe,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [
    [
      {
        provide: HTTP_INTERCEPTORS,
        useClass: HttpRequestInterceptor,
        multi: true,
      },
    ],
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
