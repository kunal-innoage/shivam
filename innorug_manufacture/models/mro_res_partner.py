from odoo import fields, models, _,api
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "res.partner"
    _description = "Res Partner"

    cost_per_yard = fields.Float("Cost Per Yard")
