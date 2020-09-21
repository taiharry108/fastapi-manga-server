import { Pipe, PipeTransform } from '@angular/core';
import { convertPySite, MangaSite } from '../manga-site.enum';

@Pipe({
  name: 'mangaSite',
})
export class MangaSitePipe implements PipeTransform {
  transform(value: string): MangaSite {
    return convertPySite(value);    
  }
}
