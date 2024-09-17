# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden Orientation"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="State",
        required=True,
        copy=False,
        default='new',
        readonly=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one('res.partner', string='Buyer', index=True, copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be canceled')
            record.state = "canceled"
        return True

    def sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('cancelled properties cannot be sold')
            record.state = "sold"
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Expected price of the property should be greater than 0'),
         ('check_selling_price', 'CHECK(selling_price > 0)',
         'Selling price of the property should be greater than 0')
    ]

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for record in self:
            if record.selling_price == 0:
                return True
            print("check_selling_price", (record.selling_price / record.expected_price))
            if (record.selling_price / record.expected_price) < 0.9:
                raise ValidationError(_('The selling price cannot be lower than 90 percent of the expected price: \n Selling price: %s, Expected price: %s') % (record.selling_price, record.expected_price))