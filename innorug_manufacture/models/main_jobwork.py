from odoo import fields, models, _, api
from datetime import date
from odoo.exceptions import UserError, ValidationError, MissingError
import logging
_logger = logging.getLogger(__name__)


class MainJobwork(models.Model):
    _name = "main.jobwork"
    _description = 'Main Job Work'
    _rec_name = "reference"
    
    
    reference = fields.Char("Reference")
    
    subcontractor_id = fields.Many2one('res.partner', string='Subcontractor')
    
    branch_id = fields.Many2one("weaving.branch", string="Branch")
    job_allotment_id = fields.Many2one("jobwork.allotment", "Job_allotement")
    
    
    work_order_ids = fields.Many2many("mrp.workorder", string="Operation")
    # sale_order_ids = fields.Many2many("sale.order", "Sale Orders")
    jobwork_allotment_ids = fields.One2many("jobwork.allotment", "jobwork_id", string="Jobwork Allotment Ids")
    
    main_cost_center_id =fields.Many2one('main.costcenter', "Cost Center")
    
    issue_date = fields.Date(string='Date Issued')
    expected_received_date = fields.Date(string='Expected Date')
    
    jobwork_line_ids  = fields.One2many("mrp.job.work","main_jobwork_id",string="Job Work Lines")
    
    alloted_material_ids = fields.One2many("subcontractor.alloted.product", "main_job_work_id", "Alloted Material")
    
    main_jobwork_components_lines = fields.One2many("main.jobwork.components.line","main_job_work_id", string="Job Work Components_line")
    
 
    
    
    state = fields.Selection([
        ('draft','DRAFT'),
        ('allotment','WAITING COMPONENTS'),
        ('release','RELEASE'),
        ('qa','PROCESS QC'),
        ('waiting_baazar','WAITING BAAZAR'),
        ('baazar','BAAZAR'),
        ('fqa','FINAL QC'),
        ('done','RECEIVED'),
        ('cancel','CANCEL')
        ], string='Status', default='draft')
    
    # Boolean Field 
    active_sub = fields.Boolean("sub")
    is_active_cost = fields.Boolean("sub")
    is_active_release = fields.Boolean("sub")
    is_active_allote = fields.Boolean("sub")
    
    @api.model
    def create(self, vals):
        if vals.get('MainJobwork', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'main.jobwork') or _('New')
        res = super(MainJobwork, self).create(vals)
        return res
    
    
       

    def delete_lines(self):
        for rec in self.jobwork_line_ids:
            if rec.product_qty ==0:
                rec.unlink()
    
     
    @api.onchange('subcontractor_id')
    def add_sub_name(self):
        for vals in self.jobwork_line_ids:
            vals.subcontractor_id = self. subcontractor_id.id
            
            
    def write(self, vals):         
        res = super(MainJobwork, self).write(vals)
        return res    
    
    
    
    def button_action_for_validate_main_job(self):
        for rec in self:
            rec.active_sub = True
            rec.state = "allotment"
            rec.is_active_allote =True
        pass
    

    def button_action_for_cost_center_main_job(self):
        self.is_active_cost = False
        self.is_active_release  = True
        if self.subcontractor_id:
            if not self.main_cost_center_id:
                self.main_cost_center_id = self.main_cost_center_id.create({
                    "main_job_work_id": self.id,
                    "subcontractor_id": self.subcontractor_id, 
                    "work_order_ids" : self.work_order_ids 
                })
            else:
                if self.main_cost_center_id.work_order_ids:
                    if self.main_cost_center_id.subcontractor_id != self.subcontractor_id:
                        self.main_cost_center_id.subcontractor_id = self.subcontractor_id               
        for rec in self.jobwork_line_ids:
            if rec.product_id and rec.product_qty > 0:
                rec.button_action_for_cost_center()
         
        pass
    
    
    def button_action_for_qa_process_main_job(self):
        pass
    
    
    def button_action_for_release_main_job(self):
        for rec in self:
            rec.is_active_release  = False
            rec.state ='release'
            for data in rec.jobwork_line_ids:
                data.button_action_for_release()
        pass
    
    
    def button_action_for_baazar_main_job(self):
        pass
    
    def button_action_for_no_amended_qty_main_job(self):
        pass
    
    
    def button_action_for_no_return_qty_main_job(self):
        pass
    
    
    def button_action_for_done_main_job(self):
        pass
    
    
    def button_action_for_cancel_main_job(self):
        pass
    
    
    def button_action_for_force_qa_main_job(self):
        pass
    
    
    
    
    
    def button_action_for_alloted_components(self):
        self.active_sub = True 
        self.get_components_allote()
        job_work_obj = self.env["mrp.job.work"]
        self.is_active_allote = False
        self.is_active_cost = True
        for rec in self.jobwork_line_ids:
            _logger.info("~~~~~~~job_work_id ~~%r~~~+++++++++++++++~~~~~",rec.id )
            if rec.product_id and rec.product_qty > 0:
                job_work_id = job_work_obj.search([('id','=', rec.id)])
                _logger.info("~~~~~~~job_work_id ~~%r~~~+++++++++++++++~~~~~",job_work_id )
                if job_work_id:
                    for line in job_work_id.subcontracter_alloted_product_ids:
                        components_id = self.env["main.jobwork.components.line"].create({
                            "alloted_product_id" : line.alloted_product_id.id,
                            "alloted_quantity" : line.alloted_quantity,
                            "amended_quantity": 0,
                            "consumed_quantity": 0,
                            "returned_quantity": 0,
                            'total_allot_qty' :  line.total_allot_qty,
                            'product_uom' : line.product_uom.id,
                            'job_work_id': rec.id,
                            "main_job_work_id": self.id,
                           })
                        if components_id :
                            self. main_jobwork_components_lines += components_id 
        return self.delete_lines()
           
                
                
                
             
    
    
    
    # def button_action_for_alloted_components(self):
    #     self.get_components_allote()
    #     job_work_obj = self.env["mrp.job.work"]
    #     for rec in self.jobwork_line_ids:
    #         _logger.info("~~~~~~~job_work_id ~~%r~~~+++++++++++++++~~~~~",rec.id )
    #         if rec.product_id and rec.product_qty > 0:
    #             for line in rec.subcontracter_alloted_product_ids:
    #                 components_id = False
    #                 if not self.main_jobwork_components_lines:
    #                     components_id = self.env["main.jobwork.components.line"].create({
    #                         "alloted_product_id" : line.alloted_product_id.id,
    #                         "alloted_quantity" : line.alloted_quantity,
    #                         "amended_quantity": 0,
    #                         "consumed_quantity": 0,
    #                         "returned_quantity": 0,
    #                         'total_allot_qty' :  line.total_allot_qty,
    #                         'product_uom' : line.product_uom.id,
    #                         'job_work_id': rec.id,
    #                         "main_job_work_id": self.id,
    #                     })
    #                 else:
    #                     if self.main_jobwork_components_lines:
    #                         for data in self.main_jobwork_components_lines:
    #                             if data.alloted_product_id == line.alloted_product_id and line.job_work_id.id == rec.id:
    #                                 data.alloted_quantity += line.alloted_quantity
    #                                 data.total_allot_qty += line.total_allot_qty
    #                             else:
    #                                 components_id = self.env["main.jobwork.components.line"].create({
    #                                     "alloted_product_id" : line.alloted_product_id.id,
    #                                     "alloted_quantity" : line.alloted_quantity,
    #                                     "amended_quantity": 0,
    #                                     "consumed_quantity": 0,
    #                                     "returned_quantity": 0,
    #                                     'total_allot_qty' :  line.total_allot_qty,
    #                                     'product_uom' : line.product_uom.id,
    #                                     'job_work_id': rec.id,
    #                                     "main_job_work_id": self.id,
    #                                 })
    #     pass
    
  
    
    def get_components_allote(self):
        for rec in self.jobwork_line_ids:
            if rec.product_id and rec.product_qty > 0:
                rec.button_action_for_allot_product()
            else:
                rec.active_org_qty_product = False
                rec.active_qty_add = False
        
    
    
    
    
    
    
class MainJobworkComponentsLine(models.Model):
    _name = "main.jobwork.components.line"
    _description = 'Main Job Work Components'
    
    
    # parent_product_id = fields.Many2one("product.product", string="Parent Product", readonly="1")
    alloted_product_id = fields.Many2one("product.product", string="Product", readonly="1")
    alloted_quantity = fields.Float("Alloted Quantity", readonly="1")
    consumed_quantity = fields.Float("Consumed Quantity")
    amended_quantity = fields.Float("Amended Qty")
    total_allot_qty = fields.Float("Total Allote Qty")
    returned_quantity = fields.Float("Returned Quantity")
    product_uom =  fields.Many2one("uom.uom",string="UOM")
    
    
    main_job_work_id = fields.Many2one("main.jobwork", string= "Main Job Work")
    
    job_work_id = fields.Many2one("mrp.job.work", string= "Job Work")    


    
    

        
                
                
    
        
        
   
    
    
    
    
    
    
    
    
    
    
    
  