#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Importing some of Google's AppEngine modules:
import os, sys, webapp2, random


sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from app.handlers import dashboard, authentication # Do not move this line above the previous sys.path.append()
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': str(random.getrandbits(128)),
}

app = webapp2.WSGIApplication([
    ('/login', authentication.Login),
    ('/project', dashboard.Project),
    ('/', dashboard.MainHandler)
], debug=True, config=config)

def main():
    app.run()

if __name__ == "__main__":
    main()
