import os
import webapp2
from app.handlers.BaseHandler import BaseHandler
import cgi, urllib, json
from google.appengine.api import urlfetch
from secrets import secrets
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User
from jinja2 import Environment, PackageLoader
from datetime import datetime
env = Environment(loader=PackageLoader('app', 'templates'))


class MainHandler(BaseHandler):
    def get(self):
        user = self.session.get("user")
        if user is None:
            self.redirect("/login")
        access_url = "https://api.github.com/user/issues?access_token=" + self.session.get("access_token") + "&filter=all&direction=dec"
        result_issues = urlfetch.fetch(url = access_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        issues = json.loads(result_issues.content)
        issueList = []
        for i in range(0,5):
            issueList.append(issues[i])
        access_url = "https://api.github.com/user/repos?access_token=" + self.session.get("access_token") + "&filter=all&sort=pushed&direction=dec"
        result_repo = urlfetch.fetch(url = access_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        five_repos = json.loads(result_repo.content)
        five_last_updated_repo_times = []
        for i in range(0, 6):
            five_last_updated_repo_times.append(five_repos[i])
        repo_time_counter = 0
        five_most_recent_commits = []
        repo_count = 1
        for repo in five_last_updated_repo_times:
            repo_date = datetime.strptime(five_last_updated_repo_times[repo_count].get('pushed_at')[0:18],"%Y-%m-%dT%H:%M:%S")
            repo_count += 1
            if len(five_most_recent_commits) == 5:
                break
            full_name = repo.get('full_name')
            access_url = "https://api.github.com/repos/" + full_name + "/commits?access_token=" + self.session.get("access_token")
            result_commit = urlfetch.fetch(url = access_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
            five_commits = json.loads(result_commit.content)
            for com_push in five_commits:
                if len(five_most_recent_commits) == 5:
                    break
                commit = com_push.get('commit')
                author = commit.get('author')
                time = datetime.strptime(author.get('date')[0:18], "%Y-%m-%dT%H:%M:%S")
                if time >= repo_date:
                    five_most_recent_commits.append(com_push)
                else:
                    repo_time_counter += 1
                    break
        print(len(five_most_recent_commits))
        template = env.get_template('index.html')
        self.response.write(template.render(name = "Dashboard", issues=issueList, commits=five_most_recent_commits, token = self.session.get("access_token"), user = User.query(User.key == self.session.get("user")).get()))


class Splash(BaseHandler):
    def get(self):
        template = env.get_template('splash.html')
        self.response.write(template.render(name = "Splash"))
        self.response.write(template.render())


class Register(BaseHandler):
    def get(self):
        template = env.get_template("registration.html")
        user = self.session.get("user")
        if user is None:
            self.response.write(template.render(name = "Registration", user = ""))
        else:
            self.response.write(template.render(name = "Registration", user = User.query(User.key == self.session.get("user")).get()))

    def post(self):
        first = cgi.escape(self.request.get('first'))
        last = cgi.escape(self.request.get('last'))
        email = cgi.escape(self.request.get('email'))
        person = User(user_id= self.session.get("username"), first_name=first, last_name= last, email= email, gravatar_url = self.session.get("gravatar") )
        person.put()
        self.session["user"] = person.key
        self.redirect("/")


class ProjectDashboard(BaseHandler):
    def get(self):
        token = self.session.get("access_token")
        if not token:
            self.redirect("/login")

        access_url = "https://api.github.com/user/repos?type=owner&access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url = access_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        project_contents = json.loads(result.content)
        template = env.get_template('project.html')
        self.response.write(template.render(name = "Project Overview", project = project_contents, user = User.query(User.key == self.session.get("user")).get()))

    def post(self):
        project_id = cgi.escape(self.request.get('id'))
        project_name = cgi.escape(self.request.get('name'))
        project_description = cgi.escape(self.request.get('desc'))
        owner = self.session.get("user")
        project = Project(project_id = int(project_id), project_title = project_name, project_desc = project_description, project_owner = owner)
        project.put()
        project_user_relation = Project_User(project_id=project.key, user_id=owner, is_owner=True)
        project_user_relation.put()
