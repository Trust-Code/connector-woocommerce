# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 - Danimar Ribeiro <danimaribeiro@gmail.com>
#    Copyright 2015 - Trust-Code - www.trustcode.com.br
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta
from openerp import models, fields, api, _
from openerp.addons.woocommerce_connect.models.Partner import partner_import_batch
from openerp.addons.connector.session import ConnectorSession

IMPORT_DELTA_BUFFER = 30

class WooBackend(models.Model):
    _name = 'woo.backend'
    _description = 'WooCommerce Backend'
    _inherit = 'connector.backend'

    _backend_type = 'woo'

    @api.model
    def select_versions(self):
        """ Available versions in the backend.
        """
        return [('2.3.11','2.3.11')]


    version = fields.Selection(selection='select_versions', required=True)
    location = fields.Char(
        string='Location',
        required=True,
        help="Url to WooCommerce",
    )
    api_key = fields.Char(
        string='Api Key',
        help="Api key to WooCommerce",
    )
    secret_api_key = fields.Char(
        string='Secret Api Key',
        help="Secret api key to WooCommerce",
    )   
    import_partners_from_date = fields.Datetime(
        string='Import partners from date',
    )
    default_lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Default Language',
        help="If a default language is selected, the records "
             "will be imported in the translation of this language.\n"
             "Note that a similar configuration exists "
             "for each storeview.",
    )
    

    @api.multi
    def import_partners(self):
        session = ConnectorSession(self.env.cr, self.env.uid,
                                   context=self.env.context)
        import_start_time = datetime.now()
        if self.import_partners_from_date:
            from_date = fields.Datetime.from_string(self.import_partners_from_date)
        else:
            from_date = None
        
        partner_import_batch.delay(
                session, 'woo.res.partner', self.id,
                {'from_date': from_date,
                 'to_date': import_start_time})
 
        next_time = import_start_time - timedelta(seconds=IMPORT_DELTA_BUFFER)
        next_time = fields.Datetime.to_string(next_time)
        self.write({'import_partners_from_date': next_time})
        return True