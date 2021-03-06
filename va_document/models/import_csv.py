import logging

from odoo import api, fields, models, _
import csv
import io
import base64

_logger = logging.getLogger(__name__)

#format (string to search, social reason name in fr_CH, lang)
SEARCH_LANG = ('fr_CH','de_CH','en_US')
SOCIAL_REASON_LANG = [
    (' SA','SA','fr_CH'),
    (' AG','SA','de_CH'),
    (' SARL','SARL','fr_CH'),
    (' Sàrl','SARL','fr_CH'),
    (' Sarl','SARL','fr_CH'),
    (' GMBH','SARL','de_CH'),
    (' GmbH','SARL','de_CH'),
]
WB_ADDRESS = {
    'full_name':0,
    'company_name':2,
    'firstname':4,
    'lastname':3,
    'street':5,
    'street2':6,
    'zip':15,
    'city':7,
    'email':11,
    'website':12,
    'phone':9,
    'mobile':10,
    'vat':13,
    'state':14,
    'country':8,
    'old_id':1,
    'customer_rank':16,
    'supplier_rank':17,
    }

class ResPartner(models.Model):

    _inherit = "res.partner"

    old_id = fields.Char()

class Document(models.Model):
    _inherit = 'documents.document'

    @api.model
    def _import_csv(self):
        self = self.sudo()
        context = self.env.context
        if context.get('active_ids'):
            docs = self.browse(context['active_ids'])
            for doc in docs:
                if self.env.ref('va_document.doctag_import_contact_pd_company') in doc.tag_ids:
                    doc.process_pipedrive_company(doc.csv_decode(';'),True)
                elif self.env.ref('va_document.doctag_import_contact_pd_person') in doc.tag_ids:
                    doc.process_pipedrive_person(doc.csv_decode(';'),True)
                elif self.env.ref('va_document.doctag_import_contact_winbiz') in doc.tag_ids:
                    #_logger.info("WINBIZ {}".format(WB_ADDRESS))
                    doc.process_winbiz(doc.csv_decode(';'),True)
                else:
                    pass
    

    def csv_decode(self,delimiter=','):
        self.ensure_one()
        decoded_data = base64.b64decode(self.attachment_id.datas)
        try:
            data = io.StringIO(decoded_data.decode("utf-8"))
            #_logger.info("WINBIZ UTF data")
        except:
            data = io.StringIO(decoded_data.decode("latin-1"))
            #_logger.info("WINBIZ latin data")
        data.seek(0)
        file_reader = []
        csv_reader = csv.reader(data, delimiter=';')
        #_logger.info("WINBIZ csv.reader")
        file_reader.extend(csv_reader)
        #_logger.info("WINBIZ file.reader")
        return file_reader

    def process_winbiz(self,data=False,force=False):
        self.ensure_one()
        if data:
            headers = data.pop(0)
            count = 0

            for item in data:
                #_logger.info("WINBIZ {}".format(item))
                count += 1
                has_subcontact = False

                company_name = item[WB_ADDRESS['company_name']]
                firstname = item[WB_ADDRESS['firstname']]
                lastname = item[WB_ADDRESS['lastname']]
                search_name = "{} {}".format(firstname,lastname)

                #common dict
                vals = {
                        'company_id': self.env.ref("base.main_company").id,
                        'street':item[WB_ADDRESS['street']],
                        'street2':item[WB_ADDRESS['street2']],
                        'zip':item[WB_ADDRESS['zip']],
                        'city':item[WB_ADDRESS['city']],
                        'email':item[WB_ADDRESS['email']],
                        'website':item[WB_ADDRESS['website']],
                        'vat':item[WB_ADDRESS['vat']],
                        'phone':item[WB_ADDRESS['phone']],
                        'mobile':item[WB_ADDRESS['mobile']],
                        'customer_rank':item[WB_ADDRESS['customer_rank']],
                        'supplier_rank':item[WB_ADDRESS['supplier_rank']],
                        'old_id':item[WB_ADDRESS['old_id']],
                        'comment':'Origin Name | {}'.format(item[WB_ADDRESS['full_name']]),
                    }
                vals.update(self.get_regional_info(item[WB_ADDRESS['state']],item[WB_ADDRESS['country']]))

                #case 1 | individual contact only
                if lastname and not company_name:
                    existing = self.env['res.partner'].search([('comment','ilike',search_name)],limit=1)
                    if not existing or force:
                        vals.update({
                            'is_company': False,
                            'company_type': 'person',
                            'type':'contact',
                            'firstname': firstname,
                            'lastname':lastname,
                        })
                
                #case 2 | company
                if company_name:
                    existing = self.env['res.partner'].search([('comment','ilike',company_name)],limit=1)
                    if not existing or force:
                        vals.update(self.pipedrive_company_name(company_name))
                        vals.update({
                                'is_company': True,
                                'company_type': 'company',
                            })
                
                #we create the 1st contact
                if existing:
                    existing.write(vals)
                    _logger.info("Contact Updated {} | {}/{}".format(existing.name,count,len(data)))
                    
                else:
                    existing = self.env['res.partner'].create(vals)
                    _logger.info("Contact Created {} | {}/{}".format(existing.name,count,len(data)))

                #company AND individual to create
                if lastname and company_name:
                    existing2 = self.env['res.partner'].search([('comment','ilike','{} {}'.format(item[WB_ADDRESS['firstname']],item[WB_ADDRESS['lastname']])),('parent_id','=',existing.id)],limit=1)
                    vals2 = {
                        'company_type': 'person',
                        'company_id': self.env.ref("base.main_company").id,
                        'parent_id': existing.id,
                        'type':'contact',
                        'firstname':firstname,
                        'lastname': lastname,
                        'customer_rank':item[WB_ADDRESS['customer_rank']],
                        'supplier_rank':item[WB_ADDRESS['supplier_rank']],
                        'comment':'Origin Name | {} {}'.format(lastname,firstname),
                    }
                    if existing2:
                        existing2.write(vals2)
                        _logger.info("Sub-Contact Updated {} | {}/{}".format(existing2.name,count,len(data)))
                        
                    else:
                        existing2 = self.env['res.partner'].create(vals2)
                        _logger.info("Sub-Contact Created {} | {}/{}".format(existing2.name,count,len(data)))

                        vals2.clear()
                        
                vals.clear()

    
    def process_pipedrive_person(self,data=False,force=False):
        self.ensure_one()
        if data:
            headers = data.pop(0)
            count = 0
            #_logger.info("{}".format(headers))
            
            for item in data:
                count += 1
                #_logger.info("0. ITEM {}".format(item))
                vals = {
                    'customer_rank':1,
                    'is_company': False,
                    'company_type': 'person',
                    'company_id': self.env.ref("base.main_company").id,
                    'type':'contact',
                }
                name = item[1]
                #we search existing contact notes to find if we already imported this one
                existing = self.env['res.partner'].search([('comment','ilike',name),('is_company','=',False)],limit=1)
                if not existing or force:

                    vals.update(self.name_to_user(item[8]))

                    #we search the parent
                    if item[7]:
                        parent = self.env['res.partner'].search([('comment','ilike',item[7]),('is_company','=',True)],limit=1)
                        if parent:
                            vals.update({
                                'parent_id':parent.id,
                                'lang':parent.lang,
                                'user_id':parent.user_id.id,
                            })

                    vals.update({
                        'name':name,
                        'function':item[3],
                        'phone':item[4],
                        'email':item[23],
                    })

                    if existing:
                        existing.write(vals)
                        _logger.info("Contact Updated {} | {}/{}".format(name,count,len(data)))
                        
                    else:
                        existing = self.env['res.partner'].create(vals)
                        _logger.info("Contact Created {} | {}/{}".format(name,count,len(data)))
                    vals.clear()

    
    def process_pipedrive_company(self,data=False,force=False):
        self.ensure_one()
        if data:
            headers = data.pop(0)
            count = 0
            #_logger.info("{}".format(headers))
            
            for item in data:
                count += 1
                #_logger.info("0. ITEM {}".format(item))
                vals = {
                    'is_company': True,
                    'company_type': 'company',
                    'company_id': self.env.ref("base.main_company").id,
                    'customer_rank':1,
                }
                name = item[1]
                #we search existing contact notes to find if we already imported this one
                existing = self.env['res.partner'].search([('comment','ilike',name),('is_company','=',True)],limit=1)
                if not existing or force:
                    vals.update(self.pipedrive_company_name(name))
                    vals.update(self.build_address(item[6],item[5]))
                    vals.update(self.get_regional_info(item[9],item[11]))
                    vals.update(self.name_to_user(item[14]))
                    vals.update(self.activity_to_industry(item[30]))
                    vals.update({
                        'city': item[8],
                        'zip': item[12],
                        'website': item[31],
                        'phone': item[32],
                        'email': item[33],
                    })
                    vals['comment'] = "{}\n{}".format(vals['comment'],item[49])
                   
                    if existing:
                        existing.write(vals)
                        _logger.info("Company Updated {} | {}/{}".format(vals['lastname'],count,len(data)))
                        
                    else:
                        existing = self.env['res.partner'].create(vals)
                        _logger.info("Company Created {} | {}/{}".format(vals['lastname'],count,len(data)))
                    
                    vals.clear()
                        

                    #second contact if any
                    if item[34]:
                        existing2 = self.env['res.partner'].search([('comment','ilike',item[34]),('parent_id','=',existing.id)],limit=1)
                        vals2 = {
                            'company_type': 'person',
                            'company_id': self.env.ref("base.main_company").id,
                            'parent_id': existing.id,
                            'customer_rank':1,
                            'type':'contact',
                            'name':item[34],
                            'city': item[41],
                            'zip': item[45],
                            'phone': item[47],
                            'email': item[48],
                            'website':item[35],
                            'comment':'Origin Name | {}'.format(item[34]),
                        }
                        vals2.update(self.build_address(item[39],item[38]))
                        vals2.update(self.get_regional_info(item[42],item[44]))
                        if existing2:
                            existing2.write(vals2)
                            _logger.info("Extra Company Updated {} | {}/{}".format(item[34],count,len(data)))
                        else:
                            existing2 = self.env['res.partner'].create(vals2)
                            _logger.info("Extra Company Created {} | {}/{}".format(item[34],count,len(data)))
                        
                        vals2.clear()

    
    def name_to_user(self, name=False):
        user = self.env['res.users'].search([('name','ilike',name)],limit=1)
        vals = {'user_id': user.id if user else False,}
        return vals

    def activity_to_industry(self, activities=False):
        activity = activities.split(',')[0] #we keep only the 1st one
        found = self.env['res.partner.industry'].search([('name','ilike',activity)],limit=1)
        vals = {'industry_id': found.id if found else False}
        return vals
    
    def get_regional_info(self,state_name=False,country_name=False):
        vals = {
            'country_id':False,
            'state_id':False,
        }
        for lang in SEARCH_LANG:
            country = self.env['res.country'].with_context(lang=lang).search([('name','ilike',country_name)],limit=1)
            if country_name and country:
                vals['country_id']=country.id
                break
        for lang in SEARCH_LANG:
            state = self.env['res.country.state'].with_context(lang=lang).search([('name','ilike',state_name)],limit=1)
            if state_name and state:
                vals['state_id']=state.id
                break
        
        return vals

    
    def build_address(self,street=False,number=False):
        if street and number:
            return {'street':"{} {}".format(street,number)}
        elif street:
            return {'street':"{}".format(street)}
        else:
            return {'street':False}

    def pipedrive_company_name(self,name = False):
        self.ensure_one()
        vals={}
        if name:
            #we set default values
            vals.update({
                'comment':'Origin Name | {}'.format(name),
                'social_reason_id': False,
                'lang': 'fr_CH',
                'name': name,
                'lastname': name,
            })
            for conf in SOCIAL_REASON_LANG:
                if conf[0] in name: #we have found a match
                    parts = name.split(conf[0])
                    new_name = "{} {}".format(parts[0],conf[1]) if len(parts)==1 \
                        else "{} {} {}".format(parts[0],parts[1],conf[1])
                    vals.update({
                        'social_reason_id': self.env['res.partner.social.reason'].search([('name','=',conf[1])],limit=1).id,
                        'lang': conf[2],
                        'name': new_name,
                        'lastname': new_name,
                    })
                    break 
        else:
            pass

        return vals
                    



