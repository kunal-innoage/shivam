from odoo import fields, models, _,api
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class BomOperationComponent(models.Model):
    _name = "bom.operation.component"
    _description = 'BOM Operation Component'

    product_qty_percentage = fields.Float("Percentage")
    is_percentage = fields.Boolean("Use %")

    operation_routing_id = fields.Many2one("mrp.routing.workcenter",string="Operation")
    
    product_bom_id = fields.Many2one(related="operation_routing_id.bom_id")
    workcenter_id = fields.Many2one(related="operation_routing_id.workcenter_id", string="Work Center")
    product_bom_line_id = fields.Many2one("mrp.bom.line", domain="[('bom_id', '=', product_bom_id)]", string="Component")
    product_id = fields.Many2one(related="product_bom_line_id.product_id", string="Product")
    product_qty = fields.Float(related="product_bom_line_id.product_qty", string="Quantity")
    product_uom_id = fields.Many2one(related="product_id.uom_id")
    
    
    
    
  