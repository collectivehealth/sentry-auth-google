from __future__ import absolute_import, print_function

from sentry.auth.view import AuthView, ConfigureView
from sentry.http import safe_urlopen, safe_urlread
from sentry.utils import json
from urllib import urlencode

from .constants import ERR_INVALID_DOMAIN, USER_DETAILS_ENDPOINT

class FetchUser(AuthView):
    def __init__(self, domain=None, *args, **kwargs):
        self.domain = domain
        super(FetchUser, self).__init__(*args, **kwargs)

    def dispatch(self, request, helper):
        access_token = helper.fetch_state('data')['access_token']

        req = safe_urlopen('{0}?{1}&alt=json'.format(
            USER_DETAILS_ENDPOINT,
            urlencode({
                'access_token': access_token,
            })
        ))

        body = safe_urlread(req)
        data = json.loads(body)

        if not data.get('data'):
            #TODO possible to sentry log this?
            print('Invalid response: %s' % body)
            return helper.error(ERR_INVALID_RESPONSE)

        if not data.get('data').get('email'):
            #TODO possible to sentry log this?
            print('Invalid response: %s' % body);
            return helper.error(ERR_INVALID_RESPONSE)

        helper.bind_state('user', data.get('data'))

        return helper.next_step()


class GoogleConfigureView(ConfigureView):
    def dispatch(self, request, organization, auth_provider):
        return self.render('sentry_auth_google/configure.html')
