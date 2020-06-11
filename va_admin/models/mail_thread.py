# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        #we avoid autosubscription from the message, but only from the add follower menu
        if not ('mail_invite_follower_channel_only' in self._context):
            return
        else:
            return super(MailThread, self).message_subscribe(partner_ids, channel_ids, subtype_ids)
