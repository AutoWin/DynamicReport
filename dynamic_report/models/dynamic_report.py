from odoo import fields, models, api, _

class dynamic_xls_report(models.TransientModel):
    _name = 'dynamic.xls.report'

    model_name = fields.Many2one('ir.model', "Model")
    field_name = fields.Many2many('ir.model.fields','rel_fields_model_rpt','wiz_id','rec_id','Field Name')
    search_domain = fields.Char("Domain")
    m2m_value = fields.Boolean('Group by', help='Select if You want the value instead of id for Many2one field')
    file_data = fields.Binary('File', readonly=True)
    file_name = fields.Char('Filename', size = 64, readonly=True)
    limit_rec = fields.Integer('Limit')
    order_type = fields.Boolean('Order',help='Check if you want the records in descending order')
    order_on_field = fields.Many2one('ir.model.fields','Order By',domain="[('model_id','=',model_name)]")
    set_offset = fields.Integer('Offset')
    domain_lines = fields.One2many('dynamic.domain.line','dynamic_rpt_id', 'Domain')
    sheet_name = fields.Char("Sheet name excel")
    header_text = fields.Char("Header text")

    @api.multi
    def get_xls(self):
        self.ensure_one()
        context = self._context
        print (context)
        model = self.model_name.model
        print(model)
        field_sel = []
        for field_name in self.field_name:
            field_sel.append(field_name.name)
        print (field_sel)
        domain = []
        for d_line in self.domain_lines:
            temp = ()
            print (type(temp))
            d_val = str(d_line.value) or False
            if d_val in ('false', 'False'):
                d_val = False
            if d_val in ('true', 'True'):
                d_val = True
            temp = (str(d_line.field_name.name), str(d_line.operator), d_val)
            domain.append(temp)
        print ('Domain: ', domain)
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'dynamic.xls.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        print (datas)
        # datas = {'ids': [], 'model': 'wizard.stock.history', 'form': {'id': 3, 'warehouse': [2], 'category': [3], 'create_uid': 1, 'create_date': '2018-12-04 07:17:42', 'write_uid': 1, 'write_date': '2018-12-04 07:17:42', 'display_name': 'wizard.stock.history,3', '__last_update': '2018-12-04 07:17:42'}}
        if context.get('xls_export'):
            print ('runrun')
            # mod_ids = self.env[model].browse([2])
            # print (mod_ids)
            # return self.env.ref('dynamic_report.dynamic_stock_xlsx').report_action(mod_ids)
            return self.env.ref('dynamic_report.dynamic_stock_xlsx').report_action(self, data=datas)

    # @api.multi
    # def print_custom_documents(self):
    #     first_report = self.env.ref('custom_module.billing_report_sample').report_action(self)
    #     return first_report
    #     invoice_obj = self.env['stock.inventory'].browse([1])
    #     return self.env.ref('stock.action_report_inventory').report_action(invoice_obj)

class dynamic_domain_line(models.TransientModel):
    _name = 'dynamic.domain.line'
    dynamic_rpt_id = fields.Many2one('dynamic.xls.report', 'Relation Field')
    field_name = fields.Many2one('ir.model.fields', 'Field Name', domain="[('model_id','=',parent.model_name)]")
    operator = fields.Selection([('ilike', 'Contains'), ('=', 'Equal'), ('!=', 'Not Equal'), ('<', 'Less Than'), ('>', 'Greater Than'),
         ('<=', 'Less Than Equal To'), ('>=', 'Greater Than Equal To')], 'Operator')
    value = fields.Char('Value', help='For relation use dot(.) with field name')



