from odoo import fields, models, _,api
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

    
class MrpQualityControl(models.Model):
    _name = 'mrp.quality.control'
    _description = 'Quality Control'
    
    name = fields.Char('Reference', default=lambda self: _('New'))
    product_id = fields.Many2one("product.product", string="Product")
    team = fields.Char("Quality Team")
    subcontractor_id = fields.Many2one('res.partner', string='Subcontractors')
    qc_manager_id = fields.Many2one('res.partner', string="QC Manager")
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
    
    active_cancel = fields.Boolean("Cancel")
    active_delayed = fields.Boolean("Delayed")
    
    

    
    
    def do_pass_qc(self):
        today = datetime.today()
        self.quality_state='pass'
        subject="PASS : "
        self.job_work_id.message_post(body=subject + str(today))
        self.job_work_id.state = "waiting_baazar"
        self.job_work_id.active_baazar =  True
        self.job_work_id.active_force_qa =  True
        self.job_work_id.active_hide_qa = True
        pass
     
    def do_fail_qc(self):
        today = datetime.today()
        subject="FAIL : "
        self.job_work_id.message_post(body=subject + str(today))
        self.job_work_id.state = "qa"
        self.quality_state='fail'
        self.job_work_id.active_baazar =  False
        pass
    

    
    
    
    

