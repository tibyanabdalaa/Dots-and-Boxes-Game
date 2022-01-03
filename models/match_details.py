from odoo import models, fields, api


class MatchDetails(models.Model):
    _name = 'match.details'
    _inherit = 'mail.thread'
    _description = 'Game Match Details'
    _rec_name = 'full_name'

    date = fields.Date(string="Date", required=True)
    player_id = fields.Many2one('player.profile', string="Player", track_visibility='True', required=True)
    country_id = fields.Many2one('res.country', related='player_id.country_id', string='Country',
                                 track_visibility='True', ondelete='restrict')

    state = fields.Selection(
        [('win', 'Win'), ('lose', 'Lose'), ('tie', 'Tie')],
        string="State", track_visibility='always')
    game_type = fields.Selection(
        [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard'), ('online', 'Online')],
        string="Game Type", track_visibility='always')

    game_point = fields.Integer(string="Game Points",
                                help="Number of boxes you have closed ", track_visibility='True')
    time_played = fields.Float(string="Time Played")
    max_sequence = fields.Integer(string="Sequence Boxes",
                                  help="Number of boxes you have closed sequentially", track_visibility='True')
    full_name = fields.Char(compute='_compute_full_name', string='Name')

    @api.depends('player_id', 'date')
    def _compute_full_name(self):
        self.full_name = " "
        if self.date and self.player_id:
            self.full_name = '%s / %s' % (self.player_id.name, self.date)
