'''
Created on Jun 19, 2015

@author: danimar
'''
from openerp import models, fields
from openerp.addons.connector.connector import (ConnectorEnvironment,
                                                install_in_connector)
from openerp.addons.connector.checkpoint import checkpoint

install_in_connector()

def add_checkpoint(session, model_name, record_id, backend_id):
    return checkpoint.add_checkpoint(session, model_name, record_id,
                                     'woo.backend', backend_id)

def get_environment(session, model_name, backend_id):
    """ Create an environment to work with. """
    backend_record = session.env['woo.backend'].browse(backend_id)
    env = Environment(backend_record, session, model_name)
    lang = backend_record.default_lang_id
    lang_code = lang.code if lang else 'pt_BR'
    if lang_code == session.context.get('lang'):
        return env
    else:
        with env.session.change_context(lang=lang_code):
            return env


class WooBinding(models.AbstractModel):
    _name = 'woo.binding'
    _inherit = 'external.binding'
    _description = 'WooCommerce Binding (abstract)'

    # 'openerp_id': openerp-side id must be declared in concrete model
    backend_id = fields.Many2one(
        comodel_name='woo.backend',
        string='Woo Backend',
        required=True,
        ondelete='restrict',
    )
    
    woocommerce_id = fields.Char(string='ID in the WooCommerce',
                            select=True)
        
    _sql_constraints = [
        ('woo_uniq', 'unique(backend_id, woocommerce_id)',
         'A binding already exists with the same WooCommerce ID.'),
    ]
    