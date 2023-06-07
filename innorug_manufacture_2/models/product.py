from odoo import fields, models, _,api
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "product.product"
    _description = "Product"

    bom_operation_component_id = fields.Many2one("bom.operation.component", "BOM Operation Component")
    design = fields.Char("Design")
    area = fields.Float("Area")
    size = fields.Char("Size")



class Product(models.Model):
    _inherit = "product.template"
    _description = "Product"

    bom_operation_component_id = fields.Many2one("bom.operation.component", "BOM Operation Component")
    design = fields.Char("Design")
    area = fields.Float("Area")
    size = fields.Char("Product Size Name")
    perimeter = fields.Float("Perimeter")
    shape = fields.Char("Shape")
    # size_type = fields.Char("Size Type")
    lenght_fraction = fields.Float("Length Fraction")

    size_type = fields.Selection([
        ('standard','Standard'),
        ('manufaturing_size','Manufaturing Size'),
        ('finishing_size','Finishing Size'),
        ('stencil','Stencil'),
        ('map','Map')
        ], string='Product Size Type')



