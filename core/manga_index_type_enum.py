from enum import Enum


class MangaIndexTypeEnum(str, Enum):
    CHAPTER = "Chapter"
    VOLUME = "Volume"
    MISC = "Misc"

m_types = list(MangaIndexTypeEnum)

def get_type_from_idx(idx: int) -> MangaIndexTypeEnum:
    return m_types[idx]