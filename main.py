from webapp2_extras import sessions

import webapp2
import login
import agenda
import grid
import calview
import member
import gig
import plan
import band
import help
import motd
import credits

config = {
  'webapp2_extras.auth': {
    'user_model': 'member.Member',
    'user_attributes': ['name', 'is_superuser']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'GABBAGABBAHEY'
  }
}

application = webapp2.WSGIApplication([
    webapp2.Route('/', agenda.MainPage, name='home'),
    webapp2.Route('/login', login.LoginPage, name='login'),
    webapp2.Route('/logout', login.LogoutHandler, name='logout'),
    webapp2.Route('/signup', login.SignupPage, name='signup'),
    webapp2.Route('/check_email', login.CheckEmail),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
                  handler=login.VerificationHandler, name='verification'),
    webapp2.Route('/<type:e>/<user_id:\d+>-<signup_token:.+>',
                  handler=login.EmailVerificationHandler, name='verification'),
    webapp2.Route('/forgot', login.ForgotPasswordHandler, name='forgot'),                  
    webapp2.Route('/password', login.SetPasswordHandler),
    webapp2.Route('/help', help.HelpHandler),
    webapp2.Route('/credits', credits.CreditsHandler),
    webapp2.Route('/seen_welcome', motd.SeenWelcomeHandler),
    webapp2.Route('/seen_motd', motd.SeenHandler),
    webapp2.Route('/agenda.html', agenda.MainPage, name='home'),
    webapp2.Route('/agenda.html', agenda.MainPage, name='agenda'),
    webapp2.Route('/agenda_switch', agenda.SwitchView),
    webapp2.Route('/grid.html', grid.MainPage),
    webapp2.Route('/calview.html', calview.MainPage),
    webapp2.Route('/member_info.html', member.InfoPage, name='memberinfo'),
    webapp2.Route('/member_edit.html', member.EditPage),
    webapp2.Route('/member_get_assocs', member.ManageBandsGetAssocs, name='getassocs'),
    webapp2.Route('/member_get_other_bands', member.ManageBandsGetOtherBands, name='getotherbands'),
    webapp2.Route('/member_new_assoc', member.ManageBandsNewAssoc, name='newassoc'),
    webapp2.Route('/member_delete_assoc.html', member.ManageBandsDeleteAssoc, name='deleteassoc'),
    webapp2.Route('/member_admin.html', member.AdminPage),
    webapp2.Route('/member_makeadmin', member.AdminMember),
    webapp2.Route('/member_delete', member.DeleteMember),
    webapp2.Route('/member_set_section', member.SetSection),
    webapp2.Route('/member_set_multi',member.SetMulti),
    webapp2.Route('/member_get_bands',member.GetBandList),
    webapp2.Route('/gig_info.html', gig.InfoPage, name="gig_info"),
    webapp2.Route('/gig_edit.html', gig.EditPage),
    webapp2.Route('/gig_archive', gig.ArchiveHandler),
    webapp2.Route('/gig_autoarchive', gig.AutoArchiveHandler),
    webapp2.Route('/gig_delete', gig.DeleteHandler),
    webapp2.Route('/gig_add_comment', gig.CommentHandler),
    webapp2.Route('/gig_get_comment', gig.GetCommentHandler),
    webapp2.Route('/print_setlist', gig.PrintSetlist),
    webapp2.Route('/print_planlist', gig.PrintPlanlist),
    webapp2.Route('/band_info.html',band.InfoPage),
    webapp2.Route('/band_edit.html',band.EditPage),
    webapp2.Route('/band_delete.html',band.DeleteBand),
    webapp2.Route('/band_get_members',band.BandGetMembers, name='getmembers'),
    webapp2.Route('/band_get_sections',band.BandGetSections, name='getsections'),
    webapp2.Route('/band_new_section',band.NewSection),
    webapp2.Route('/band_delete_section',band.DeleteSection),
    webapp2.Route('/band_move_section',band.MoveSection),
    webapp2.Route('/band_confirm_member',band.ConfirmMember),
    webapp2.Route('/band_makeadmin', band.AdminMember),
    webapp2.Route('/band_removemember', band.RemoveMember),
    webapp2.Route('/band_admin.html', band.AdminPage),   
    webapp2.Route('/band_get_member_list',band.GetMemberList),
    webapp2.Route('/band_nav.html',band.BandNavPage),
    webapp2.Route('/band_get_upcoming', band.GetUpcoming),
    webapp2.Route('/calevents', calview.CalEvents),
    webapp2.Route('/updateplan', plan.UpdatePlan),
    webapp2.Route('/updateplancomment', plan.UpdatePlanComment),
    webapp2.Route('/updateplansection', plan.UpdatePlanSection),
    webapp2.Route('/motd_admin.html', motd.AdminPage)
], config=config, debug=True)