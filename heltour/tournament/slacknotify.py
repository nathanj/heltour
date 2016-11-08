import requests
from heltour import settings
from collections import namedtuple
import slackapi
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

_events = {'mod': ['user_registered', 'user_latereg_created', 'user_withdrawl_created', 'lonepairing_forfeit_changed']}

def _send_notification(event_type, league, text):
    for ln in league.leaguenotification_set.all():
        if event_type in _events[ln.type]:
            slackapi.send_message(ln.slack_channel, text)

def _abs_url(url):
    site = Site.objects.get_current().domain
    return 'https://%s%s' % (site, url)

def user_registered(reg):
    league = reg.season.league
    reg_url = _abs_url(reverse('admin:review_registration', args=[reg.pk]) + '?_changelist_filters=status__exact%3Dpending%26season__id__exact%3D' + str(reg.season.pk))
    list_url = _abs_url(reverse('admin:tournament_registration_changelist') + '?status__exact=pending&season__id__exact=' + str(reg.season.pk))
    pending_count = reg.season.registration_set.filter(status='pending', season=reg.season).count()
    message = '@%s has <%s|registered> for %s. <%s|%d pending>' % (reg.lichess_username, reg_url, league.name, list_url, pending_count)
    _send_notification('user_registered', league, message)

def latereg_created(latereg):
    league = latereg.round.season.league
    manage_url = _abs_url(reverse('admin:manage_players', args=[latereg.round.season.pk]))
    message = '@%s <%s|added> for round %d' % (latereg.player.lichess_username, manage_url, latereg.round.number)
    _send_notification('user_latereg_created', league, message)

def withdrawl_created(withdrawl):
    league = withdrawl.round.season.league
    manage_url = _abs_url(reverse('admin:manage_players', args=[withdrawl.round.season.pk]))
    message = '@%s <%s|withdrawn> for round %d' % (withdrawl.player.lichess_username, manage_url, withdrawl.round.number)
    _send_notification('user_withdrawl_created', league, message)

def lonepairing_forfeit_changed(pairing):
    league = pairing.round.season.league
    white = pairing.white.lichess_username if pairing.white is not None else '?'
    black = pairing.black.lichess_username if pairing.black is not None else '?'
    message = '@%s vs @%s %s' % (white, black, pairing.result or '*')
    _send_notification('lonepairing_forfeit_changed', league, message)