import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MangaIndexComponent } from './ui/manga-index/manga-index.component';
import { MainComponent } from './ui/main/main.component';
import { ProfileComponent } from './ui/user/profile/profile.component';
import { FavoriteComponent } from './ui/user/favorite/favorite.component';
import { HistoryComponent } from './ui/user/history/history.component';


const routes: Routes = [
  {path: 'manga-index', component: MangaIndexComponent},
  {path: '', component: MainComponent},
  { path: 'profile', component: ProfileComponent },
  { path: 'favorite', component: FavoriteComponent },
  { path: 'history', component: HistoryComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
