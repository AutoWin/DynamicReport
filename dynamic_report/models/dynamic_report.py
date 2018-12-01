from odoo import fields, models, api, _

class dynamic_xls_report(models.Model):
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


class dynamic_domain_line(models.Model):
    _name = 'dynamic.domain.line'
    dynamic_rpt_id = fields.Many2one('dynamic.xls.report', 'Relation Field')
    field_name = fields.Many2one('ir.model.fields', 'Field Name', domain="[('model_id','=',parent.model_name)]")
    operator = fields.Selection([('ilike', 'Contains'), ('=', 'Equal'), ('!=', 'Not Equal'), ('<', 'Less Than'), ('>', 'Greater Than'),
         ('<=', 'Less Than Equal To'), ('>=', 'Greater Than Equal To')], 'Operator')
    value = fields.Char('Value', help='For relation use dot(.) with field name')

