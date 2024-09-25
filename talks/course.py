#!/usr/bin/env python

import os
import sys
import textwrap
from travo import GitLab
from travo.jupyter_course import JupyterCourse
from travo.script import main
from travo.utils import run


class Info111(JupyterCourse):
    def ensure_work_dir(self):
        """
        Ensure the existence of the student's work directory

        In this implementation, the work dir is initialized as a clone
        of the course's ComputerLab repo.

        If already a clone, try to update the work dir with a pull,
        and ignore failures.

        Fails if the work dir is already a git directory pointing elsewhere.
        """
        project = self.forge.get_project(f"{self.path}/ComputerLab")
        project.clone_or_pull(self.work_dir(),
                              force=True,
                              pull_can_fail=True,
                              anonymous=True)

    init = ensure_work_dir

    def start(self) -> None:
        """
        Ouvre le tableau de bord du cours en local avec JupyterLab
        """
        self.ensure_work_dir()
        run(["jupyter", "lab", "tableau_de_bord.md"],
            cwd=self.work_dir())

    def clone(self, assignment: str) -> None:
        """
        Clone the assignment repo in the student work dir
        """
        self.ensure_work_dir()
        assignment_repo = self.assignment(assignment).repo()
        path = self.work_dir(assignment=assignment)
        self.forge.git(["clone", assignment_repo.http_url_to_repo, path])

    def compile(self, *args: str, **kwargs: None) -> None:
        """Lance le compilateur C++ avec des arguments standards"""
        args = ("clang++",
                "-g", "-Wall", "-pedantic",
                "-Wno-sign-compare", "-Wno-unused-value",
                "-std=c++17",
                *os.environ.get("CPPFLAGS", "").split(),
                *os.environ.get("LDFLAGS", "").split(),
                *args)
        # args = ["clang",
        #         "-g", "-Wall", "-pedantic",
        #         "-Wno-sign-compare", "-Wno-unused-value",
        #         "-std=c++11"] + \
        #     os.environ.get("CPPFLAGS", "").split() + \
        #     os.environ.get("LDFLAGS", "").split() + \
        #     list(args)
        self.run(*args)

    def reformat(self, *args: str, **kwargs: None) -> None:
        self.run("astyle",
                 "--style=java",
                 "--indent=spaces", "--indent=spaces=4",
                 "--indent-switches",
                 "--indent-namespaces",
                 "--indent-modifiers",
                 "--indent-col1-comments",
                 "--min-conditional-indent=0",
                 "--pad-oper",
                 "--pad-header",
                 "--align-pointer=name",
                 "--align-reference=name",
                 "--keep-one-line-statements",
                 "--convert-tabs",
                 "--close-templates",
                 "--break-after-logical",
                 "--max-code-length=78",
                 *args)

setattr(Info111, "g++", Info111.compile)

# env)
#     cd $COURSE_ROOT/binder
#     git pull
#     travo_run conda env $1
#     travo_run ./postBuild
#     exit 0;;


# forge = GitLab("https://gitlab.dsi.universite-paris-saclay.fr/")
forge = GitLab("https://gitlab-research.centralesupelec.fr/")
course = Info111(forge=forge,
                 path="Info111",
                 name="Info 111 Programmation Impérative",
                 url="https://Nicolas.Thiery.name/Enseignement/Info111",
                 student_dir="./",
                 session_path="2024-2025",
                 group_submissions=True,
                 expires_at="2025-12-31",
                 jobs_enabled_for_students=True,
                 student_groups=["MI1", "MI2", "MI3", "MI4",
                                 "LDDIM1", "LDDIM2",
                                 "LDDMP1", "LDDMP2",
                                 "EcoMath", "MathSV",
                                 "AuditeursLibres"],
                 # assignments=["Semaine1",
                 #              "Semaine2",
                 #              "Semaine3",
                 #              "Semaine4",
                 #              "Semaine5",
                 #              "Semaine6",
                 #              "Semaine7",
                 #              "Semaine8",
                 #              "Semaine9",
                 #              "Semaine10",
                 #              "Projet-DonneesLibres",
                 #              "Projet-MixMoEnDuplicata"]
                 )

assert course.student_groups is not None
course.script = sys.argv[0]
if course.script.endswith("info-111"):
    course.student_dir = "~/ProgImperative"
    course.script = "info-111"

usage = f"""Aide pour l'utilisation de la commande {course.script}
===============================================

Télécharger ou mettre à jour un TP ou projet (remplacer «Semaine1» par
le nom du TP):

    {course.script} fetch Semaine1

Déposer un TP ou projet (remplacer «Semaine1» par le nom du TP ou
projet et remplacer «Groupe» par le nom de votre groupe):

    {course.script} submit Semaine1 Groupe

{textwrap.fill('Groupes: '+', '.join(course.student_groups))}

Lancer le tableau de bord (inutile sur le service JupyterHub):

    {course.script} start

Compiler un programme (ici essai.cpp):

    {course.script} compile essai.cpp -o essai

Plus d'aide:

    {course.script} --help
"""

if __name__ == "__main__":
    main(course, usage)
