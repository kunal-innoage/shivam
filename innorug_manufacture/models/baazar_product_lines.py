from odoo import fields, models, _, api
import logging
_logger = logging.getLogger(__name__)



class BaazaProductLines(models.Model):
    _name = "mrp.baazar.product.lines"
    _description = 'Baazar Product Lines'

    name = fields.Char(string="Baazar Product Lines")
    job_work_id = fields.Many2one("mrp.job.work", string="Job Work")

    subcontractor_id = fields.Many2one(related="job_work_id.subcontractor_id",string="Subcontractor")
    manager_id = fields.Many2one(related="job_work_id.manager_id",string="Manager")
    product_id =fields.Many2one(related="job_work_id.product_id", string="Product")
    cost_center_id = fields.Many2one(related ="job_work_id.cost_center_id", string="Cost Center")
    product_qty = fields.Float(related ="job_work_id.product_qty", string="Product Qty")
    pending_qty = fields.Integer(related ="job_work_id.pending_product_qty", string="Total Pending Qty")
    receive_product_qty =fields.Integer(string="Received Qty")
    accepted_qty = fields.Integer("Accepted Qty")
    rejected_qty = fields.Integer("Rejected Qty")
    
    state = fields.Selection([
        ('draft','DRAFT'),
        ('process','PROCESS'),
        ('done','WAITING FOR VERIFY'),
        ('verify','VERIFIED'),
        ], string='Status',  default='draft')


    mrp_production_id = fields.Many2one(related="job_work_id.mrp_production_id", string="Production")
    
    
    #quality Check
    quality_control_id = fields.Many2one("mrp.quality.control", string="Quality Check")
    
     #original details of product
    design = fields.Char(related = "job_work_id.design", string="Design", readonly="1")
    area = fields.Float(related="job_work_id.area", string="Area", readonly="1")
    size = fields.Char(related="job_work_id.size", string="Product Size Name", readonly="1")
    perimeter = fields.Float(related="job_work_id.perimeter", string="Perimeter", readonly="1")
    shape = fields.Char(related="job_work_id.shape", string="Shape", readonly="1")
    lenght_fraction = fields.Float(related="job_work_id.lenght_fraction", string="Length Fraction", readonly="1")
    size_type = fields.Selection(related="job_work_id.size_type", string='Product Size Type', readonly="1")



    #Actual details of product
    actual_weight = fields.Float("Actual Weight")
    actual_design = fields.Char("Actual Design")
    actual_area = fields.Float("Actual Area")
    actual_size = fields.Char("Actual Product Size Name")
    actual_perimeter = fields.Float( "Actual Perimeter")
    actual_shape = fields.Char("Actual Shape")
    # size_type = fields.Char("Size Type")
    actual_lenght_fraction = fields.Float("Actual Length Fraction")

    actual_size_type = fields.Selection([
        ('standard','Standard'),
        ('manufaturing_size','Manufaturing Size'),
        ('finishing_size','Finishing Size'),
        ('stencil','Stencil'),
        ('map','Map')
        ], string=' Actual Product Size Type')
    
    
    total_receive_weight = fields.Float("Exoected Receive Weight") 
    
    
    
    def do_confirm(self):
        for baazar_line in self:
            baazar_line.state = 'process'
        return self.do_open_wizards()
        pass
    
    def do_process(self):
        self.job_work_id.state = 'waiting_baazar'
        self.job_work_id.state = 'baazar'
        self.state ="done"
        self.rejected_qty = 0
        self.rejected_qty =  self.receive_product_qty - self.accepted_qty
        self.total_receive_weight = 0
        if self.job_work_id.product_qty >0:
                w = self.job_work_id.total_weight / self.job_work_id.product_qty
                self.total_receive_weight = w * self.accepted_qty
        return  self.do_open_wizards()
    
    
    

    
    
    def do_open_wizards(self):
        self.ensure_one() 
        return {
            'type': 'ir.actions.act_window',
            'name': _("Product Lines"),
            'view_mode': 'form',
            # 'view_ids': [(self.env.ref('innorug_manufacture.view__mrp_job_work_form')).id],
            'res_model': 'mrp.baazar.product.lines',
            'res_id': self.id,
            "target" : "new",
        }
 
        pass
    
    
    def now_verify(self):
        self.state =  'verify'
        return self.job_work_id.calculate_total_receive_product_qty()  
        


   