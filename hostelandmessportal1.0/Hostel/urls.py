from django.conf.urls import include,url
from . import views
app_name='hostel'

urlpatterns = [
	 url(r'^$',views.homepage,name='homepage'),
	url(r'hostelcomplaintadmin/$', views.caretakerhostelcomplaint ,name = "caretaker"),
	url(r'^inout/$', views.inOutIndex ,name = "inOut"),
	url(r'^hostel_complaint/$', views.HostelComplaintIndex ,name = "HostelComplaint") ,
	url(r'^guestentry/$', views.GuestEntryIndex ,name = "Guestentry"),
	url(r'^roomregistration/$', views.registration_form ,name = "roomregistration"),
        url(r'^auth/callback/(?P<token>.+)/$',views.login_view,name='login'),
	url(r'^logout',views.logout_view,name='logout'), ]


