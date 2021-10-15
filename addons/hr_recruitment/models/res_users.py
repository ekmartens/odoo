# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class ResUsers(models.Model):
    _inherit = 'res.users'

    def _create_recruitment_interviewers(self):
        if not self:
            return
        interviewer_group = self.env.ref('hr_recruitment.group_hr_recruitment_interviewer')
        recruitment_group = self.env.ref('hr_recruitment.group_hr_recruitment_user')

        interviewer_group.sudo().write({
            'users': [
                (4, user.id) for user in self - recruitment_group.users
            ]
        })

    def _remove_recruitment_interviewers(self):
        if not self:
            return
        interviewer_group = self.env.ref('hr_recruitment.group_hr_recruitment_interviewer')
        recruitment_group = self.env.ref('hr_recruitment.group_hr_recruitment_user')

        job_interviewers = self.env['hr.job'].read_group([('interviewer_ids', 'in', self.ids)], ['interviewer_ids'], ['interviewer_ids'])
        user_ids = {j['interviewer_ids'][0] for j in job_interviewers}

        application_interviewers = self.env['hr.applicant'].read_group([('interviewer_id', 'in', self.ids)], ['interviewer_id'], ['interviewer_id'])
        user_ids |= {a['interviewer_id'][0] for a in application_interviewers}

        # Remove users that are no longer interviewers on at least a job or an application
        users_to_remove = set(self.ids) - (user_ids | set(recruitment_group.users.ids))
        interviewer_group.sudo().write({
            'users': [
                (3, user_id) for user_id in users_to_remove
            ]
        })
