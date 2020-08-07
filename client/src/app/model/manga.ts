import { Chapter } from './chapter';

export interface Manga {
    name: string;
    url: string;
    chapters: Map<string, Chapter[]>;
    finished: boolean;
    thumImg: string;
    lastUpdate: string;
}
