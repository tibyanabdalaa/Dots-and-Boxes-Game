# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class GamePlayersProfile(models.Model):
    _name = 'player.profile'
    _inherit = 'mail.thread'
    _description = 'Players Profile'

    name = fields.Char(string="Name", required=True, track_visibility='True')
    image = fields.Image("Image", max_width=1024, max_height=1024, store=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', track_visibility='True')
    phone = fields.Char()
    email = fields.Char()

    points = fields.Integer(string="Points",
                            help="points as the number of boxes you have closed", compute='calc_games_data')
    games_played = fields.Integer(string="Games Played", compute='calc_games_data')
    games_win = fields.Integer(string="Games Won", compute='calc_games_data', store=True)
    games_lose = fields.Integer(string="Games Lose", compute='calc_games_data', store=True)
    games_tie = fields.Integer(string="Games Tie", compute='calc_games_data', store=True)

    win_percentage = fields.Float(string="Win Percentage", compute='calc_win_percentage')
    time_played = fields.Float(string="Time Played", help='Total Time Played', compute='calc_games_data')
    average_match_time = fields.Float(string="Average Match Time", compute='calc_average_match_time')
    min_victory_time = fields.Float(string="Min Victory Time", compute='calc_games_data')

    max_boxes = fields.Integer(string="Max Boxes",
                               help="Max number of boxes you have closed", compute='calc_max_boxes')
    max_sequence = fields.Integer(string="Max Sequence",
                                  help="Max number of boxes you have closed sequentially", compute='calc_max_sequence')
    matches_count = fields.Integer(default=0, compute="_matches_count")

    def _matches_count(self):
        for rec in self:
            matches = self.env['match.details'].search([('player_id', '=', rec.id)])
            rec.matches_count = len(matches)

    def calc_games_data(self):
        for rec in self:
            rec.points = 0
            rec.games_played = 0
            rec.games_win = 0
            rec.games_lose = 0
            rec.games_tie = 0
            rec.time_played = 0
            rec.min_victory_time = 0
            matches = self.env['match.details'].search([('player_id', '=', rec.id)], order="time_played ASC")
            if matches:
                rec.points = sum(matches.mapped('game_point'))
                rec.games_played = len(matches)
                rec.games_win = len(matches.filtered(lambda l: l.state == "win"))
                rec.games_lose = len(matches.filtered(lambda l: l.state == "lose"))
                rec.games_tie = len(matches.filtered(lambda l: l.state == "tie"))
                rec.time_played = sum(matches.mapped('time_played'))
                rec.min_victory_time = matches[0].mapped('time_played')[0]

    def calc_max_boxes(self):
        for rec in self:
            rec.max_boxes = 0
            matches = self.env['match.details'].search([('player_id', '=', rec.id)], order="game_point desc")
            if matches:
                rec.max_boxes = matches[0].mapped('game_point')[0]

    def calc_max_sequence(self):
        for rec in self:
            rec.max_sequence = 0
            matches = self.env['match.details'].search([('player_id', '=', rec.id)], order="max_sequence desc")
            if matches:
                rec.max_sequence = matches[0].mapped('max_sequence')[0]

    @api.depends('games_played', 'games_win')
    def calc_win_percentage(self):
        for rec in self:
            rec.win_percentage = 0
            if rec.games_played and rec.games_win:
                rec.win_percentage = rec.games_played / rec.games_win

    @api.depends('games_played', 'time_played')
    def calc_average_match_time(self):
        for rec in self:
            rec.average_match_time = 0
            if rec.games_played and rec.time_played:
                rec.average_match_time = rec.games_played / rec.time_played

    def match_details_view(self):
        return {
            'name': 'Matches',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'match.details',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('player_id', '=', self.id)],
            'context': {'player_id': self.id}
        }

    def action_view_last_game(self):
        matches = self.env['match.details'].search([('player_id', '=', self.id)], order="date desc", limit=1)
        if matches:
            return {
                'name': 'Last Game',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'match.details',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [('id', '=', matches.id)],
                'target': 'current',
            }
        else:
            raise ValidationError("This Player hasn't any Games")
