from odoo import fields, models, _
import logging
_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'



    job_order_id = fields.Many2one("mrp.job.work", "Job Order")
    rug_work_order_id = fields.Many2one("mrp.workorder", " Rug Work Order")


    def get_job_order_id_job_work(self):
        if self.product_id:
            if not self.job_order_id:
                self.job_order_id = self.job_order_id.create({
                    "mrp_production_id": self.id,
                    "product_id": self.product_id,
                    'qty_production' : self.product_qty
                })
            else:
                if self.job_order_id.mrp_production_id:
                    if self.job_order_id.product_id != self.product_id:
                        self.job_order_id.product_id = self.product_id
                        self.job_order_id.qty_production = self.product_qty
                else:
                    self.job_order_id.mrp_production_id = self.id
        return self.view_job_order_action()



    def view_job_order_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Job Work"),
            'view_mode': 'list,form,kanban',
            # 'view_ids': [(self.env.ref('innorug_manufacture.mrp_job_work_view_kanban').id, 'kanban')],
            'res_model': 'mrp.job.work',
            # 'context': {
            #     'search_default_order_logs': 1,
            # },
            'domain': [('mrp_production_id','=',self.id)]
        }

    

    def action_view_mrp_job_work(self):
        for rec in self.move_raw_ids:
            _logger.info("~~~~~~2~~~~~~%r~~~~rec~~~~",rec.product_uom_qty )
        if self.product_id:
            if not self.job_order_id:
                self.job_order_id = self.job_order_id.create({
                    "mrp_production_id": self.id,
                    "product_id": self.product_id,
                    'qty_production' : self.product_qty
                })
            else:
                if self.job_order_id.mrp_production_id:
                    if self.job_order_id.product_id != self.product_id:
                        self.job_order_id.product_id = self.product_id
                        self.job_order_id.qty_production = self.product_qty
                else:
                    self.job_order_id.mrp_production_id = self.id
        return self.view_job_order_action()