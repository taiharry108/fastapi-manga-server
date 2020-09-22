import { Chapter } from './chapter';

export interface Manga {
    id: number;
    name: string;
    url: string;
    chapters: Map<string, Chapter[]>;
    finished: boolean;
    thum_img: string;
    last_update: string;
    site?: string;
    latest_chapters?: Map<string, Chapter>;
    is_fav?: boolean;
}

export interface MangaSimple {
    id: number;
    isFav: boolean;
}