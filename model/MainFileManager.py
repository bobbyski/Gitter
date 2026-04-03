import json
from dataclasses import asdict

from model.MainFile import MainFile
from model.Project import Project


class MainFileManager:
    shared = MainFile("untitled")

    @classmethod
    def save_shared_to_json(cls, path: str):
        data = {
            "name": cls.shared.name,
            "projects": [asdict(project) for project in cls.shared.projects],
        }

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @classmethod
    def load_shared_from_json(cls, path: str):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        loaded = MainFile(data.get("name", "untitled"))
        loaded.projects = [
            Project( project_data.get("name", ""),
                     project_data.get("directory", ""),
                     project_data.get("status", ""),
                     project_data.get("tagBranch", "master"),
                     project_data.get("issuePrefixes", [] ),
                     project_data.get("prPatterns", [] ),
                     project_data.get("commits", [] ),
                     project_data.get("issues", [] ),
                     project_data.get("releases", [] ),
                     project_data.get("groups", [] ),
                     project_data.get("favorite", False )
                     )
            for project_data in data.get("projects", [])
        ]

        cls.shared = loaded

        loaded.sort_projects()

        return cls.shared
