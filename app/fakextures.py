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
        if Requirements.query().count() == 0:
            Fakextures.install_requirements()
        if Task.query().count() == 0:
            Fakextures.install_tasks()
        if Event_LK.query().count() == 0:
            Fakextures.install_event_lk()

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
                 gravatar_url="https://avatars.githubusercontent.com/u/8582482?v=3"),
            User(user_id="interlochen", first_name="Ryan", last_name="Dooley", email="rcd53@nau.edu",
                 gravatar_url="https://avatars.githubusercontent.com/u/3316388?v=3")
        ]
        ndb.put_multi(users)

        print "Users installed"

    @staticmethod
    def install_projects():
        project = Project(project_id=31822394, project_title="cs399_final", project_desc="NAU CS 399 Final Project",
                          project_owner=User.query(User.user_id == "c1phr").get(use_cache=False).key)
        project.put()

        print "Projects installed"

    @staticmethod
    def install_user_projects():
        project = Project.query(Project.project_id == 31822394).get(use_cache=False).key
        for user in User.query().iter(keys_only=True):
            project_user = Project_User(project_id=project, user_id=user)
            project_user.put()

        print "User_Project Relations Installed"

    @staticmethod
    def install_requirements():
        title = "Github Issue Tracking System"
        descr = "Building a system to track the issues from Github and potentially convert them to requirements."
        requirement = Requirements(req_title = title, req_desc = descr,
                                   project_id=Project.query(Project.project_id ==31822394).get(use_cache=False).key)
        requirement.put()
        event = Events(user = User.query(User.user_id == "dukeayers").get(use_cache=False).key, project = Project.query(Project.project_id ==31822394).get(use_cache=False).key,  event_type = Event_LK.query(Event_LK.event_code == 3).get().key, description = title + " - " + descr, event_relation_key = None).put()

        title = "Reporting System Tools"
        descr = "Find a way to use the reporting system to our advantage."
        requirement = Requirements(req_title = title, req_desc = descr,
                                   project_id=Project.query(Project.project_id ==31822394).get(use_cache=False).key)
        requirement.put()
        event = Events(user = User.query(User.user_id == "c1phr").get(use_cache=False).key, project = Project.query(Project.project_id ==31822394).get(use_cache=False).key,  event_type = Event_LK.query(Event_LK.event_code == 3).get().key, description = title + " - " + descr, event_relation_key = None).put()

        title = "Appease the Web Dev Gods"
        descr = "We might need a lamb..."
        requirement = Requirements(req_title = title, req_desc = descr,
                                   project_id=Project.query(Project.project_id ==31822394).get(use_cache=False).key)
        requirement.put()
        event = Events(user = User.query(User.user_id == "dukeayers").get(use_cache=False).key, project = Project.query(Project.project_id ==31822394).get(use_cache=False).key,  event_type = Event_LK.query(Event_LK.event_code == 3).get().key, description = title + " - " + descr, event_relation_key = None).put()

        print "Requirements Installed"


    @staticmethod
    def install_tasks():
        requirement = Requirements.query().fetch(1, keys_only=True)
        task = Task(task_title = "Transfer issue into task", requirement = requirement[0],
                                   task_desc= "Build something cool", assignee = User.query(User.user_id == "dukeayers").get(use_cache=False).key)
        task.put()

        print "Requirements Installed"

    @staticmethod
    def install_event_lk():
        event_lks = [
            Event_LK(event_code=1, event_type="Task Status"),
            Event_LK(event_code=2, event_type="Task Created"),
            Event_LK(event_code=3, event_type="Requirement Created"),
            Event_LK(event_code=4, event_type="Commit"),
            Event_LK(event_code=5, event_type="Project Team Changed")
        ]
        ndb.put_multi(event_lks)

        print "Event LK Installed"
