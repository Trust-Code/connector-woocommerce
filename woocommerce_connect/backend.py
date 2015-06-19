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

import openerp.addons.connector.backend as backend

woo = backend.Backend('WooCommerce')
woo23 = backend.Backend(parent=woo, version='2.3.11')


