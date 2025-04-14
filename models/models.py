class ExeFile:
    def __init__(self, id: int, exe_file_path: str, created_at: str):
        self.id = id
        self.exe_file_path = exe_file_path
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            exe_file_path=data.get("exe_file_path"),
            created_at=data.get("created_at")
        )