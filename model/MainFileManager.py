import json
from dataclasses import asdict
from model.MainFile import MainFile
from model.Project import Project

EXCLUDED_PROJECT_FIELDS = {"commits", "issues", "releases", "status"}

class MainFileManager:
    shared = MainFile("untitled")

    @classmethod
    def save_shared_to_json(cls, path: str):
        output = MainFile(MainFileManager.shared.name)

        for project in MainFileManager.shared.projects:
            node = Project(project.name, project.directory, "", project.tagBranch, project.issuePrefixes, project.prPatterns, project.favorite, [],[],[],[] )
            node.favorite = project.favorite
            output.add_project(node)

        with open(path, "w", encoding="utf-8") as file:
            json.dump( asdict( output ), file, indent=2)

    @classmethod
    def load_shared_from_json(cls, path: str):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            loaded = MainFile(data.get("name", "untitled"))
            loaded.projects = [
                Project(
                    name=project_data.get("name", ""),
                    directory=project_data.get("directory", ""),
                    status="",
                    tagBranch=project_data.get("tagBranch", "master"),
                    issuePrefixes=project_data.get("issuePrefixes", []),
                    prPatterns=project_data.get("prPatterns", []),
                    favorite=project_data.get("favorite", False),
                    groups=project_data.get("groups", []),
                    commits=[],
                    issues=[],
                    releases=[],
                )
                for project_data in data.get("projects", [])
            ]

            cls.shared = loaded
            loaded.sort_projects()

        except Exception:
            loaded = MainFile("untitled")

        return cls.shared

    @classmethod
    def update_all_projects(cls):
        for project in cls.shared.projects:
            project.update()
        cls.shared.sort_projects()
