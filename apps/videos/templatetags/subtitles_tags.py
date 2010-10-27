# Universal Subtitles, universalsubtitles.org
# 
# Copyright (C) 2010 Participatory Culture Foundation
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see 
# http://www.gnu.org/licenses/agpl-3.0.html.

from django import template
from videos.forms import SubtitlesUploadForm, PasteTranscriptionForm
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('videos/_upload_subtitles.html', takes_context=True)
def upload_subtitles(context, video):
    context['video'] = video
    initial = {}
    if 'language' in context:
        initial['language'] = context['language'].language    
    context['form'] = SubtitlesUploadForm(context['user'], initial=initial)
    return context

@register.inclusion_tag('videos/_paste_transcription.html', takes_context=True)    
def paste_transcription(context):
    #It is just template of pop-up, you should add link with 'upload-transcript-button' class
    initial = {}
    if 'language' in context:
        initial['language'] = context['language'].language

    context['form'] = PasteTranscriptionForm(context['user'], initial=initial)
    return context

@register.simple_tag
def complete_indicator(language):
    if language.is_original or language.is_forked:
        v = language.version()
        return _('%(count)s Lines') % {'count': v and v.subtitle_set.count() or 0}
    return '%i %%' % language.percent_done

@register.simple_tag
def complete_color(language):
    if language.is_original or language.is_forked:
        return 'full'
    
    val = language.percent_done
    if val >= 95:
        return 'eighty'
    elif val >= 80:
        return 'sixty'
    elif val >= 30:
        return 'fourty'
    else:
        return 'twenty'