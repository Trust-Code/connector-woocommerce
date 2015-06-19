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

from openerp import models, fields, api, _

class WooBackend(models.Model):
    _name = 'woo.backend'
    _description = 'WooCommerce Backend'
    _inherit = 'connector.backend'

    _backend_type = 'woo'

    @api.model
    def select_versions(self):
        """ Available versions in the backend.
        """
        return [('2.3', '2.3+')]


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
    
