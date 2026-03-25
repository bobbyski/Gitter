from dataclasses import dataclass
from model.Project import Project

@dataclass
class MainFile:
    name: str
    projects: list[Project]

    def __init__(self, name: str):
        self.name = name
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)
        self.sort_projects()

    def remove_project(self, project):
        if project in self.projects:
            self.projects.remove(project)

    def sort_projects(self):
        self.projects.sort(key=lambda project: (project.name.lower(), project.directory.lower()))

    def __repr__(self):
        return f"MainFile(name='{self.name}', projects={len(self.projects)} projects)"

    def setupSampleData(self):
        self.name = "Bobby's Projects"
        self.projects = []

        self.projects = [
            Project(f"Project {i}", f"/path/to/project_{i.lower()}")
            for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ]
        # Adding a few more to reach 30
        self.projects.extend([
            Project("Project Aardvark Adventures with the amazing Andrew Abernathy", "/path/to/project_aa"),
            Project("Project BB", "/path/to/project_bb"),
            Project("Project CC", "/path/to/project_cc"),
            Project("Project DD", "/path/to/project_dd"),
            Project("Project EE", "/path/to/project_ee"),
            Project("Project FF", "/path/to/project_ff"),
            Project("Project GG", "/path/to/project_gg"),

            # add a long text place holde rto test limits
            Project("Project HH", """We the People of the United States, in order to form a more perfect union, 
                                  establish justice, insure domestic tranquility, provide for the common defense, 
                                  promote the general welfare, and secure the blessings of liberty to ourselves and 
                                  our posterity, do ordain and establish this Constitution for the United States of 
                                  America.
                                  """)
        ])

