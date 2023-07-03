from odoo import fields, models, _, api
from datetime import date
from odoo.exceptions import UserError, ValidationError, MissingError
import logging
_logger = logging.getLogger(__name__)



class JobworkAllotment(models.Model):
    _name = "jobwork.allotment"
    _description = 'Jobwork Allotment'
    
    branch_id = fields.Many2one("weaving.branch", string="Branch")
    
    
    branch_lines_ids = fields.One2many("weaving.branch","jobwork_id", string="Branch")
    
    product_id = fields.Many2one(related ="work_order_id.production_bom_id", string="Product")
    product_qty = fields.Integer("Original Quantity")
    alloted_product_qty = fields.Integer("Alloted Quantity")
    remaining_product_qty = fields.Integer("Remaining Quantity")
    
    issue_date = fields.Date(string='Issued Date')
    expected_received_date = fields.Date(string='Expected Date')
    
    division = fields.Selection([
        ('kelim','KELIM'),
        ('knotted','KNOTTED'),
        ('main','MAIN'),
        ('sample','SAMPLE'),
        ('shag','SHAG'),
        ('tufted','TUFTED')
        ], string='Division')
    
    
    allotment = fields.Selection([
        ('to_do','To Do'),
        ('partial','Partially Alloted'),
        ('full','Fully Alloted'),
        ], string='Status')
    
    work_order_id = fields.Many2one("mrp.workorder", "Work Order")
    operation_id = fields.Many2one(related='work_order_id.workcenter_id', string="Operation")
    mo_order_id = fields.Many2one(related="work_order_id.production_id", string="Manufacturing Order")
    sale_order_id = fields.Char("Sale Order")
    
    jobwork_id = fields.Many2one("main.jobwork" ,string= "Main Job")
    jobwork_line_ids = fields.One2many(related="jobwork_id.jobwork_line_ids" ,string= "Job Work Lines")

    
    def create(self, vals):
        res = super(JobworkAllotment, self).create(vals)
        _logger.info("~~~~~~~res1~~~sss~~%r~~~~~~~~",res)
        for job_allotment in res:
            job_allotment.remaining_product_qty = job_allotment.product_qty
        return res    
    
   

    
    
    
    
    def map_job_work_allotement_order_record(self):
        _logger.info("~-------~~self        %r    ........",self.product_id)
        # WO not from multiple branch 
        branch_obj = self.env["weaving.branch"]
        allotment_obj = self.env["jobwork.allotment"]
        to_include = []
        to_add_branch_id = False
        for allotment_line in self:
            if allotment_line.branch_id not in branch_obj:
                branch_obj += allotment_line.branch_id
            if allotment_line.allotment != "full":
                allotment_obj += allotment_line
                to_add_branch_id = allotment_line.branch_id
        _logger.info("~-------~~       %r    ........",self.product_id)
                
        allotment_obj_ids = allotment_obj
        work_order_ids = [line.work_order_id.id for line in allotment_obj_ids]
        _logger.info("~~~~~~~to_add_branch_id        %r     allotment_obj    %r  ..work_order_ids    %r    .......",to_add_branch_id, allotment_obj, work_order_ids)

        if len(branch_obj ) != 1:
            raise UserError(_("Please Select Only Single Branch "))  
            # Validation error 
            return False
        else:
            branch_obj = branch_obj[0]
        _logger.info("~-------~~self    %r    .........", allotment_obj_ids.product_id )
        
      
        
        # Create Main Job Work 
        main_job_work_id = self.env["main.jobwork"].create({
            'branch_id' : allotment_obj_ids.branch_id.id ,
            'work_order_ids':  [(6, 0, [v for v in work_order_ids])],
            # 'jobwork_allotment_ids': [(6, 0, [line.id for line in allotment_obj_ids])]
        })
     
    
        _logger.info("~~~~~~~main_job_work_id        %r    .........",main_job_work_id)
        _logger.info("~~~~~~~self        %r    .........",self.product_id)
        # Add job work lines
        if main_job_work_id:
            job_work_line_ids = self.env['mrp.job.work']
            for line in allotment_obj_ids:
                job_work_line_ids += self.env["mrp.job.work"].create({
                    "mrp_production_id": line.mo_order_id.id,
                    "mrp_work_order_id": line.work_order_id.id,
                    "main_jobwork_id" : main_job_work_id.id,
                    "original_product_qty": line.remaining_product_qty if line.alloted_product_qty else line.product_qty ,
                    "product_id" : line.product_id.id,
                    "division": line.division,
                    "active_qty_add" : True,
                    "active_org_qty_product" : True,
                    "jobwork_allotment_id" : line.id
                })
                # line.jobwork_ids += main_job_work_id
        return self.get_action_main_branch(main_job_work_id)
    
    
    def get_action_main_branch(self, main_job_work_id):
        return {
            'type': 'ir.actions.act_window',
            'name': _("Main Job Work"),
            'view_mode': 'form',
            'res_model': 'main.jobwork',
            'res_id': main_job_work_id.id,
            "target" : "current",
        }   
        
        
        
        
   