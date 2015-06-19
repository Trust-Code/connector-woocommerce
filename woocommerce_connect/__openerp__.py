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

{
    'name': 'Connector for WooCommerce',
     'version': '0.1',
     'category': 'Connector',
     'author': "Trust-Code - Danimar Ribeiro",
     'website': 'http://www.trustcode.com.br',
     'license': 'AGPL-3',
     'depends': [
            'connector', 'connector_ecommerce'
     ],
     'data': [    
        'views/woo_model_view.xml'
     ],
     'installable': True,
 }
