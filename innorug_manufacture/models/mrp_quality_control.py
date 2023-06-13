from odoo import fields, models, _,api
import logging
_logger = logging.getLogger(__name__)


class MrpQualityCheck(models.Model):
    _inherit = 'quality.check'


    job_work_id = fields.Many2one("mrp.job.work", string="Job Work" )

    active_cancel = fields.Boolean("Cancel")
    active_delayed = fields.Boolean("Delayed")
    subcontractor_id = fields.Many2one('res.partner', string='Subcontractors')
    state_job = fields.Selection(related='job_work_id.state')
    





    def do_pass(self):
        self.job_work_id.state = "waiting_baazar"
        self.job_work_id.active_baazar =  True
        self.job_work_id.active_force_qa =  True
        self.job_work_id.active_hide_qa = True
        return super(MrpQualityCheck, self).do_pass()
     
    def do_fail(self):
        self.job_work_id.state = "qa"
        self.job_work_id.active_baazar =  False
        return super(MrpQualityCheck, self).do_fail()
    







    @api.model_create_multi
    def create(self,vals):
        _logger.info("~~TEST~~~~2~~~~~~~~~l~"  )
        result = super(MrpQualityCheck,self).create(vals)
        # _logger.info("~~~~~~2~~~~~%r~~~~~~l~",result.job_work_id  )
        # for res in result.job_work_id:
        #     result.product_id = res.product_id
        #     _logger.info("~~~~~~2~~~~~~%r~~~~rec~~~~",rec )
        #     pass
        #     # if res:
        #     #     res.line_id = res.id
        #     #     res.warehouse_id = self.env.context.get('warehouse_id')
        #     #     res.shop_id = self.env.context.get('shop_id')
        #     # if res.product_ref and res.product_ref.startswith('='):
        #     #     res.product_ref = res.product_ref[2:]
        #     #     res.product_ref = res.product_ref[:-1]
        return result
    
class MrpQualityControl(models.Model):
    _name = 'mrp.quality.control'
    _description = 'Quality Control'
    
    name = fields.Char('Reference', default=lambda self: _('New'))
    product_id = fields.Many2one("product.product", string="Product")
    team = fields.Char("Quality Team")
    subcontractor_id = fields.Many2one('res.partner', string='Subcontractors')
    type = fields.Selection([
        ('instructions','Instructions'),
        ('take_a_picture','Take a Picture'),
        ('pass_fail','Pass - Fail'),
        ('measure','Measure'),
        ], string='Type')
    quality_state = fields.Selection([
        ('none', 'To do'),
        ('pass', 'Passed'),
        ('fail', 'Failed')], string='Status',
        default='none')
    control_date = fields.Datetime('Control Date')
  
    picking_id = fields.Many2one('stock.picking', 'Picking')
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('product_id', '=', product_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    user_id = fields.Many2one('res.users', 'Responsible')
    note = fields.Html('Notes')
    picture = fields.Binary('Picture', attachment=True)
    additional_note = fields.Text(
        'Additional Note', help="Additional remarks concerning this check.")
    
    
    # Job work details
    job_work_id = fields.Many2one("mrp.job.work", string="Job Work" )
    production_id = fields.Many2one(related='job_work_id.mrp_production_id', string="Production")
    state_job = fields.Selection(related='job_work_id.state')
    operation_id = fields.Many2one(related='job_work_id.work_center_id', string="Operation")
    
    
    def do_pass_qc(delf):
        pass
    
    
    def do_fail_qc(self):
        pass

    
    
    
    

