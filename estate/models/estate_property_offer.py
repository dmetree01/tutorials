# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - date.today().date()).days

    def accept_offer(self):
        for record in self:
            if not record.status:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
            
        offers = self.env['estate.property.offer'].search([])
        for offer in offers:
            if not offer.status:
                offer.status = "refused"
        return True

    def refuse_offer(self):
        for record in self:
            print(record.status)
            if not record.status:
                record.status = "refused"
        return True