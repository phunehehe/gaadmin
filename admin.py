# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
#
# The Original Code is GAAdmin.
#
# The Initial Developer of the Original Code is Hoang Xuan Phu.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Hoang Xuan Phu.
#
# Alternatively, the contents of this file may be used under the terms
# of the GNU General Public License version 3 or later
# (the "GPL License"), in which case the
# provisions of the GPL License are applicable instead of those
# above.  If you wish to allow use of your version of this file only
# under the terms of the GPL License and not to allow others to use
# your version of this file under the MPL, indicate your decision by
# deleting  the provisions above and replace  them with the notice and
# other provisions required by the GPL License.  If you do not delete
# the provisions above, a recipient may use your version of this file
# under either the MPL or the GPL License.


from mechanize import LinkNotFoundError
from zope.testbrowser.browser import Browser
import itertools
import re


class Administrator():
    '''An automated Google Apps administrator.'''


    def __init__(self, domain, username, password):
        '''Create an administrator, then log in with the given credentials.'''
        self.domain = domain
        self.browser = Browser()
        self.login(username, password)


    def login(self, username, password):
        '''Log in with the given username and password.'''

        self.browser.open('https://www.google.com/a/%s/ServiceLogin' % self.domain)
        form = self.browser.getForm(id='gaia_loginform')

        # domain is automatically added
        form.getControl(name='Email').value = username
        form.getControl(name='Passwd').value = password
        form.submit()


    def go_to_group(self, group):
        '''Open the groups's page.'''
        self.browser.open('https://www.google.com/a/cpanel/%s/Group?groupId=%s' % (self.domain, group))


    def users_in_group(self, group):
        '''Return the set of users in the group.'''

        self.go_to_group(group)
        pattern = re.compile('<td>(\\S+@.\\S+)</td>')

        # Add all users in the current (first page).
        users = set(re.findall(pattern, self.browser.contents))
        try:
            # Go to next pages and add all of them.
            while True:
                self.browser.getLink(text='Next').click()
                users.update(re.findall(pattern, self.browser.contents))
        except LinkNotFoundError:
            pass

        return users


    def add_user_to_group(self, user, group):
        '''Add the user to the group.

        Currently only one user is added at a time.

        '''

        self.go_to_group(group)

        form = self.browser.getForm(id='addmember')
        form.getControl(name='members').value = user
        # Click this button to submit the form
        form.getControl(name='add').click()

