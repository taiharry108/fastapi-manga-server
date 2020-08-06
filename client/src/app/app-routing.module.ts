import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MangaIndexComponent } from './ui/manga-index/manga-index.component';


const routes: Routes = [
  {path: "manga-index", component: MangaIndexComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
