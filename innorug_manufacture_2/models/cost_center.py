from odoo import fields, models, _, api
import logging
_logger = logging.getLogger(__name__)



class CostCenter(models.Model):
    _name = "mrp.cost.center"
    _description = 'Cost Center'
    _rec_name = "mrp_production_id"

    # @api.model
    # def default_get(self, fields):
    #     res = super(CostCenter, self).default_get(fields)
    #     order = self.env['mrp.workorder'].search([('subcontractor_ids','=',self._context.get('subcontractor_ids'))])     
    #     res.update({'subcontractor_ids': order.subcontractor_ids.name})
    #     _logger.info("~~~~~~~~~~~~%r~~~~~~res~~", res)
    #     return res


    name = fields.Char(string="Cost Center")
    job_work_id = fields.Many2one("mrp.job.work", string="Job Work")

    subcontractor_id = fields.Many2one(related="job_work_id.subcontractor_id",string="Subcontractor")
    product_id =fields.Many2one(related="job_work_id.product_id", string="Product")
    product_qty = fields.Float(related="job_work_id.product_qty", string="Allotment Qty(Units)")
    work_center_id = fields.Many2one(related="job_work_id.work_center_id",string="Work Center")


    mrp_production_id = fields.Many2one(related="job_work_id.mrp_production_id", string="MRP Production")


    issue_date = fields.Date(related="job_work_id.issue_date", string='Issued Date')
    expected_received_date = fields.Date(related="job_work_id.expected_received_date", string='Expected Received Date')
    total_day = fields.Integer(related="job_work_id.total_day", string='Total Days')

    time_incentive = fields.Float("Time Incentive")
    time_penalities = fields.Float("Time Penality")
    fragments = fields.Char("Fragments")

  




    