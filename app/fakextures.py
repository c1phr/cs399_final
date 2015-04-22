from app.models.models import *

# Class to fake a fixture system of having default data
class Fakextures():
    def __init__(self):
        pass

    @staticmethod
    def install_fixtures(delete_all=False):
        if delete_all:
            Fakextures.clear_datastore()
        if User.query().count() == 0:
            Fakextures.install_users()
        if Project.query().count() == 0:
            Fakextures.install_projects()
        if Project_User.query().count() == 0:
            Fakextures.install_user_projects()

    @staticmethod
    def clear_datastore():
        # Remember to delete in order that foreign keys agree with to avoid errors
        ndb.delete_multi(Requirements.query().fetch(keys_only=True))
        ndb.delete_multi(Project_User.query().fetch(keys_only=True))
        ndb.delete_multi(Project.query().fetch(keys_only=True))
        ndb.delete_multi(User.query().fetch(keys_only=True))

    @staticmethod
    def install_users():
        users = [
            User(user_id="c1phr", first_name="Ryan", last_name="Batchelder", email="ryanbatch@gmail.com",
                 gravatar_url="https://avatars.githubusercontent.com/u/543635?v=3"),
            User(user_id="dukeayers", first_name="Duke", last_name="Ayers", email="dfa24@nau.edu",
                 gravatar_url="https://avatars.githubusercontent.com/u/6547941?v=3"),
            User(user_id="salbottig", first_name="Salvatore", last_name="Bottiglieri", email="sb797@nau.edu",
                 gravatar_url="https://avatars.githubusercontent.com/u/6665173?v=3"),
            User(user_id="cmh553", first_name="Christopher", last_name="Heiser", email="cmh553@nau.edu",
                 gravatar_url="https://avatars.githubusercontent.com/u/8582482?v=3")
        ]
        ndb.put_multi(users)

        print("Users installed")

    @staticmethod
    def install_projects():
        project = Project(project_id=31822394, project_title="cs399_final", project_desc="NAU CS 399 Final Project",
                          project_owner=User.query(User.user_id == "c1phr").get(use_cache=False).key)
        project.put()

        print("Projects installed")

    @staticmethod
    def install_user_projects():
        project = Project.query(Project.project_id == 31822394).get(use_cache=False).key
        for user in User.query().iter(keys_only=True):
            project_user = Project_User(project_id=project, user_id=user)
            project_user.put()

        print("User_Project Relations Installed")

    @staticmethod
    def install_requirements():
        pass