#coding=utf-8
'''
Created on Jun 19, 2015

@author: danimar
'''
from openerp import models, fields, api
from woocommerce_connect.service.WooCommerceClient import WooCommerceClient
from woocommerce_connect.connector import get_environment
from woocommerce_connect.backend import woo
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from openerp.addons.connector.unit.synchronizer import Importer
from openerp.addons.connector.unit.mapper import (mapping,
                                                  only_create,
                                                  ImportMapper
                                                  )




class MagentoResPartner(models.Model):
    _name = 'woo.res.partner'
    _inherit = 'woo.binding'
    _inherits = {'res.partner': 'openerp_id'}
    _description = 'WooCommerce Partner'

    _rec_name = 'name'

    openerp_id = fields.Many2one(comodel_name='res.partner',
                                 string='Partner',
                                 required=True,
                                 ondelete='cascade')

    created_at = fields.Datetime(string='Created At (on WooCommerce)',
                                 readonly=True)
    updated_at = fields.Datetime(string='Updated At (on WooCommerce)',
                                 readonly=True)
    emailid = fields.Char(string='E-mail address')
    newsletter = fields.Boolean(string='Newsletter')
    guest_customer = fields.Boolean(string='Guest Customer')
    
class ResPartner(models.Model):
    _inherit = 'res.partner'

    woo_bind_ids = fields.One2many(
        comodel_name='woo.res.partner',
        inverse_name='openerp_id',
        string="Magento Bindings",
    )
    birthday = fields.Date(string='Birthday')
    company = fields.Char(string='Company')

    @api.model
    def _address_fields(self):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set.
        """
        fields = super(ResPartner, self)._address_fields()
        fields.append('company')
        return fields
    
@woo
class PartnerAdapter(CRUDAdapter):
    _model_name = 'woo.res.partner'
    _woo_model = 'customers'
    _admin_path = '/{model}/{id}'

    def create(self, values):
        return self._call('%s.create' % self._woo_model, values)
    
    def search(self, filters=None):
        """ Search records according to some criterias
        and returns a list of ids """        
        return self._call('%s.search' % self._woo_model, values)

    def read(self, id, attributes=None):
        """ Returns the information of a record """        
        return self._call('%s.read' % self._woo_model, values)

    def search_read(self, filters=None):
        """ Search records according to some criterias
        and returns their information"""        
        return self._call('%s.search_read' % self._woo_model, values)

    def write(self, id, data):
        """ Update records on the external system """        
        return self._call('%s.write' % self._woo_model, values)

    def delete(self, id):
        """ Delete a record on the external system """        
        return self._call('%s.delete' % self._woo_model, values)




@woo
class PartnerBatchWooImporter(Importer):
    """ Synchronize the WooCommerce Partners.
    """
    _model_name = ['woo.res.partner']

    def run(self, filters=None):
        """ Run the synchronization """
        print "Sincronização vai iniciar"
        
        wc_client = WooCommerceClient('ck_5e5692af317c09ca4581be6bc5596714', 
                                  'cs_3115cf0868e4ae29117257e13cec6248', 
                                  'http://127.0.0.1:8080/wordpress')
        customers = wc_client.get_customers()
        for customer in customers:
            print str(customer)



@woo
class PartnerImportMapper(ImportMapper):
    _model_name = 'woo.res.partner'

    direct = [
        ('email', 'email'),
        ('dob', 'birthday'),
        ('email', 'emailid'),
        ('taxvat', 'taxvat'),
        ('group_id', 'group_id'),
    ]

    @only_create
    @mapping
    def is_company(self, record):
        # partners are companies so we can bind
        # addresses on them
        return {'is_company': True}

    @mapping
    def names(self, record):
        # TODO create a glue module for base_surname
        parts = [part for part in (record['firstname'],
                                   record['middlename'],
                                   record['lastname']) if part]
        return {'name': ' '.join(parts)}

    @mapping
    def customer_group_id(self, record):
        # import customer groups
        binder = self.binder_for(model='magento.res.partner.category')
        category_id = binder.to_openerp(record['group_id'], unwrap=True)

        if category_id is None:
            raise MappingError("The partner category with "
                               "magento id %s does not exist" %
                               record['group_id'])

        # FIXME: should remove the previous tag (all the other tags from
        # the same backend)
        return {'category_id': [(4, category_id)]}

    @mapping
    def website_id(self, record):
        binder = self.binder_for(model='magento.website')
        website_id = binder.to_openerp(record['website_id'])
        return {'website_id': website_id}

    @only_create
    @mapping
    def company_id(self, record):
        binder = self.binder_for(model='magento.storeview')
        storeview = binder.to_openerp(record['store_id'], browse=True)
        if storeview:
            company = storeview.backend_id.company_id
            if company:
                return {'company_id': company.id}
        return {'company_id': False}

    @mapping
    def lang(self, record):
        binder = self.binder_for(model='magento.storeview')
        storeview = binder.to_openerp(record['store_id'], browse=True)
        if storeview:
            if storeview.lang_id:
                return {'lang': storeview.lang_id.code}

    @only_create
    @mapping
    def customer(self, record):
        return {'customer': True}

    @mapping
    def type(self, record):
        return {'type': 'default'}

    @only_create
    @mapping
    def openerp_id(self, record):
        """ Will bind the customer on a existing partner
        with the same email """
        partner = self.env['res.partner'].search(
            [('email', '=', record['email']),
             ('customer', '=', True),
             '|',
             ('is_company', '=', True),
             ('parent_id', '=', False)],
            limit=1,
        )
        if partner:
            return {'openerp_id': partner.id}



@job(default_channel='root.woo')
def partner_import_batch(session, model_name, backend_id, filters=None):
    """ Prepare the import of partners modified on WooCommerce """
    if filters is None:
        filters = {} 
    env = get_environment(session, model_name, backend_id)
    importer = env.get_connector_unit(PartnerBatchWooImporter)
    importer.run(filters=filters)

    
    
