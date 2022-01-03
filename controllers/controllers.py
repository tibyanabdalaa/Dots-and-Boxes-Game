# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DotsGame(http.Controller):
    @http.route('/dots_game/api/view_matches/', method='GET', type="json", auth='public')
    def read_help_data(self, **kw):
        help_data = request.env['config.details'].sudo().search([])
        return help_data.read(['help_data'])

    @http.route('/dots_game/api/view_matches/', method='GET', type="json", auth='public')
    def view_matches(self, **kw):
        matches = request.env['player.profile'].sudo().search([('id', '=', request.params['id'])])
        return matches.read(['id', 'points', 'games_played', 'games_win', 'games_lose',
                             'games_tie', 'win_percentage', 'time_played', 'average_match_time',
                             'min_victory_time', 'max_boxes', 'max_sequence'
                             ])

    @http.route("/dots_game/api/create_player", method='POST', csrf=False, type="json", auth='user')
    def create_player(self, **kw):
        create_player = request.env['player.profile'].sudo().create({
            'name': request.params['name'],
            'image': request.params['image'],
            'country_id': request.params['country_id'],
            'phone': request.params['phone'],
            'email': request.params['email'],
        })
        return True

    @http.route("/dots_game/api/create_match", method='POST', csrf=False, type="json", auth='user')
    def create_match(self, **kw):
        create_match = request.env['match.details'].sudo().create({
            'date': request.params['date'],
            'player_id': request.params['player_id'],
            'country_id': request.params['country_id'],
            'game_type': request.params['game_type'],
            'game_point': request.params['game_point'],
            'time_played': request.params['time_played'],
            'max_sequence': request.params['max_sequence'],
            'state': request.params['state'],
        })
        return True
