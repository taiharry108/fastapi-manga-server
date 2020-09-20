import { Pipe, PipeTransform } from '@angular/core';
import { MangaSite } from '../manga-site.enum';

@Pipe({
  name: 'mangaSite',
})
export class MangaSitePipe implements PipeTransform {
  transform(value: string): MangaSite {
    let site: MangaSite;
    switch (value) {
      case 'manhuaren': {
        site = MangaSite.ManHuaRen;
        break;
      }
      case 'manhuagui': {
        site = MangaSite.ManHuaGui;
        break;
      }
      case 'manhuadb': {
        site = MangaSite.ManHuaDB;
        break;
      }
      case 'manhuabei': {
        site = MangaSite.ManHuaBei;
        break;
      }
      case 'comicbus': {
        site = MangaSite.ComicBus;
        break;
      }      
    }
    return site;    
  }
}
