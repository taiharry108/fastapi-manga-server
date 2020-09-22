from enum import Enum


class CrudEnum(str, Enum):
    Created = "created"
    Updated = "updated"
    Deleted = "deleted"
    Failed = "failed"
