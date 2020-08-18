import { Chapter } from './chapter';

export interface Manga {
    name: string;
    url: string;
    chapters: Map<string, Chapter[]>;
    finished: boolean;
    thum_img: string;
    last_update: string;
}
