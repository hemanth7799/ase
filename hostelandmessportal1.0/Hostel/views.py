# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals
from Hostel.models import Student,MobileNo,RoomRegistration,HostelComplaint,InOutList,GuestEntry
from django.http import Http404
from django.shortcuts import get_object_or_404,render
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from Hostel.forms import RoomRegistrationForm
from django.contrib.auth.models import User
import requests,json
from django.shortcuts import redirect
#from django.contrib.auth.models import AbstractUser
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg','pdf']
def login_view(request,token):                                                                                        
	res = requests.post(url='https://serene-wildwood-35121.herokuapp.com/oauth/getDetails', data={'token': token,'secret': 'ff5bbfae032e66f2abdb15b113bfab5d3f1741b1ed1f60b04e7062d74024bad29f57b82e6cfe0eee53ee6e595405c00907af0179c85c2c0c396e6e3df1f250a7'})
	res = json.loads(res.content)
	#email = res['student'][0]['Student_Email']	
	rollno = res['student'][0]['Student_ID']
	rollno = 'S' + str(rollno)
	if(User.objects.filter(username=str(rollno)).exists()):
		user = authenticate(request,username=rollno, password='5412417')
		#print(user,rollno,'5412417')
		if user is not None:
			if user.is_active:
				login(request,user)
				print(request.user)
				return redirect('/hostel/')
 			else:
				return render(request, 'Hostel/login.html', {'status': 'Your account has been disabled'})
	else:
		student_obj = Student()
		student_obj.rollno = rollno
		student_obj.first_name = res['student'][0]['Student_First_Name']
		student_obj.last_name = res['student'][0]['Student_Last_name']
		student_obj.middle_name = res['student'][0]['Student_Middle_Name']
		student_obj.regis_year = 2016
		student_obj.gender = res['student'][0]['Student_Gender']
		student_obj.curr_year = res['student'][0]['Student_Cur_YearofStudy']
		student_obj.regis_deg = res['student'][0]['Student_Registered_Degree']
		student_obj.regis_deg_dur = res['student'][0]['Student_Registered_Degree_Duration']
		student_obj.curr_sem = res['student'][0]['Student_Cur_Sem']
		student_obj.blood_grp = res['student'][0]['Student_Blood_Group']     
		user = User.objects.create_user(username=rollno,email=res['student'][0]['Student_Email'],password='5412417')
		user.save()
		user_id_obj = user
		#user_id = user_id_obj['user_id']
		print(user_id_obj)
		print('-----------------------------------------------')
        
		student_obj.user = user_id_obj
		student_obj.save()
		user = authenticate(request,username=rollno, password='5412417')
		print(user,rollno,'5412417')
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect('/hostel/')
		else:
			return render(request, 'Hostel/login.html', {'status': 'Your account has been disabled'})
			print(email)
		if email:
			return render(request,'Hostel/index.html')
def logout_view(request):
	logout(request)
	return render(request,'Hostel/index2.html')
def homepage(request):
	if request.user.is_authenticated():
		return render(request,'Hostel/index.html')
	else:
		return render(request,'Hostel/index2.html')
def inOutIndex(request):
	form={}
	if request.user.is_authenticated() :
  # if this is a POST request we need to process the form data
		if request.method == 'POST':
    # create a form instance and populate it with data from the request:
			in_time= request.POST['in_time']
			out_time = request.POST['out_time']
			out_place=request.POST['out_place']
			out_reason=request.POST['out_reason']
			print(in_time)
			print(out_time)
			usr=User.objects.get(username=request.user.username)
			stud=Student()
			stud=Student.objects.get(user=usr)
		
			in_out=InOutList()
			in_out.student=stud
			in_out.in_time=in_time
			in_out.out_time=out_time
			in_out.out_place=out_place
			in_out.out_reason=out_reason
			in_out.save()
			#return HttpResponse('data stored in db')
		context={'text':0}
			
		return render(request, 'Hostel/hostelleave.html',context)
	else:
		context={'text':0}
		return render(request, 'Hostel/login.html',context)
def HostelComplaintIndex(request):
	form={}
	if request.user.is_authenticated() :
  # if this is a POST request we need to process the form data
		if request.method == 'POST':
    # create a form instance and populate it with data from the request:
			#complain_time= request.POST['complain_time']
		
			complaint=request.POST['complaint']
			usr=User.objects.get(username=request.user.username)
			stud=Student()
			stud=Student.objects.get(user=usr)
		#stud.save()
			hos_compl=HostelComplaint()
			hos_compl.student=stud
			hos_compl.complaint=complaint
		#hos_compl.complain_time=complain_time

			hos_compl.save()
			#return HttpResponse('data stored in db')
		context={'text':0}
			
		return render(request, 'Hostel/hostelcomplaint.html',context)
	else:
		context={'text':0}
		return render(request, 'Hostel/login.html',context)
def GuestEntryIndex(request):
	form={}
	if (request.user.is_authenticated() ):
  # if this is a POST request we need to process the form data
		if request.method == 'POST':
    # create a form instance and populate it with data from the request:
			guest_gender= request.POST['guest_gender']
			guest_name = request.POST['guest_name']
			guest_age=request.POST['guest_age']
			no_of_days=request.POST['no_of_stay']
			usr=User.objects.get(username=request.user.username)
			stud=Student()
			stud=Student.objects.get(user=usr)
		
			guest_entry=GuestEntry()
			guest_entry.student=stud
			guest_entry.guest_gender=guest_gender
			guest_entry.guest_name=guest_name
			guest_entry.guest_age=guest_age
			guest_entry.no_of_stay=no_of_days
			guest_entry.save()
			#return HttpResponse('data stored in db')
		context={'text':0}
			
		return render(request, 'Hostel/guestentry.html',context)
	else:
		context={'text':0}
		return render(request, 'Hostel/login.html',context)
def registration_form(request):
	print('venkat')
	form=RoomRegistrationForm(request.POST or None,request.FILES or None)
	if request.user.is_authenticated() :
		
		if request.method == 'POST':
			
			if form.is_valid():
				
	 			try:
					form = RoomRegistrationForm(request.POST, request.FILES)
					usr=User.objects.get(username=request.user.username)
					stud=Student()
					stud=Student.objects.get(user=usr)
					
			

        		
            			
            				room_no=request.POST.get('pref_room_no')
					
					hos_name=request.POST.get('hostel_name')
					print(hos_name)
					if(len(RoomRegistration.objects.filter(pref_room_no=room_no))>1 and len(RoomRegistration.objects.filter(hostel_name=hos_name))>1 ):
						return HttpResponseRedirect('/hostel/roomregistration')
	   				roomregis=RoomRegistration()
	    				roomregis.pref_room_no=room_no
	    				roomregis.fee_proof=request.FILES.get('fee_proof')
	    				roomregis.hostel_name=hos_name
	    				roomregis.student=stud
					file_type = roomregis.fee_proof.url.split('.')[-1]
            				file_type = file_type.lower()
           				if file_type not in IMAGE_FILE_TYPES:
                				context = {
                    			
                    			'error_message': 'Image file must be PNG, JPG, or JPEG',
                			}
                				return render(request, 'Hostel/roomregistration.html', context)
            				roomregis.save()
            				#return HttpResponse('data stored in db')
				except:
					context = {
                    			
                    			'message': 'You have already registered for room',
                			}
					return render(request, 'Hostel/roomregistration.html', context)
    			else:
        			form = RoomRegistrationForm()
    		return render(request, 'Hostel/roomregistration.html', {
        'form': form
})
	else:
		context={'text':0}
		return render(request, 'Hostel/login.html',context)
def caretakerhostelcomplaint(request):
	k=len(HostelComplaint.objects.all())
	hostel_Complaint=[]
	student=[]
	complain_time=[]
	hostelcomplaint_data=HostelComplaint.objects.all().order_by('complain_time')
	
	room_regis=RoomRegistration.objects.all()
	m=len(RoomRegistration.objects.all())
	l=0
	for i in hostelcomplaint_data:
		for j in room_regis:
			if(i.student==j.student):
				k=i.complain_time
				k=str(k)
				k=k.split('+')
				hostel_Complaint.append(str(i.student))
				hostel_Complaint.append(str(i.complaint))
				hostel_Complaint.append(str(k[0]))
				hostel_Complaint.append(str(j.pref_room_no))
				
				hostel_Complaint.append(str(j.hostel_name))
				
			
	hostelcomplaint_data=HostelComplaint.objects.all().order_by('complain_time')
	
	listoflist=[]
	for row in range(len(hostel_Complaint)/5):
		innerlist=[]
		for col in range(5):
			innerlist.append(hostel_Complaint[row*5+col])
		listoflist.append(innerlist)
	print(listoflist)
	
	context2={'hostel_complaint':listoflist}
	return render(request,'Hostel/hostelcomplaintAdmin.html',context2)
	
def caretakerguestentry(request):
	k=len(GuestEntry.objects.all())
	Guest_Entry=[]
	student=[]
	complain_time=[]
	guestentry_data=GuestEntry.objects.all().order_by('complain_time')
	
	room_regis=RoomRegistration.objects.all()
	m=len(RoomRegistration.objects.all())
	l=0
	for i in guestentry_data:
		for j in room_regis:
			if(i.student==j.student):
				
				Guest_Entry.append(str(i.student))
				Guest_Entry.append(str(i.guest_gender))
				Guest_Entry.append(str(i.no_of_stay))
				Guest_Entry.append(str(i.guest_name))
				Guest_Entry.append(str(i.guest_age))
				Guest_Entry.append(str(i.relation))
				Guest_Entry.append(str(j.pref_room_no))
				
				Guest_Entry.append(str(j.hostel_name))
				
			
	guestentry_data=GuestEntry.objects.all().order_by('pref_room_no')
	
	listoflist=[]
	for row in range(len(Guest_Entry)/5):
		innerlist=[]
		for col in range(5):
			innerlist.append(Guest_Entry[row*5+col])
		listoflist.append(innerlist)
	print(listoflist)
	
	context2={'guest_entry':listoflist}
	return render(request,'Hostel/guestentryadmin.html',context2)
	



