export enum MangaSite {
  ManHuaRen = '漫畫人',
  ManHuaDB = '漫畫DB',
  ManHuaGui = '漫畫櫃',
  ManHuaBei = '漫畫唄',
  ComicBus = '8Comic',
}

export const convertPySite = (value: string): MangaSite => {
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
};
