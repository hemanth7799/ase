from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import RefundForm,FeedbackForm
from django.contrib.auth import get_user_model
from Hostel.models  import Student,RoomRegistration
from Mess.models import Refund,MessFeedback
User = get_user_model()

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg','pdf']

def homepage(request):
	return render(request,'Mess/index.html')
def messmenu(request):
	return render(request,'Mess/messmenu.html')
def refund(request):
    if not request.user.is_authenticated():
        return render(request, 'Mess/login.html')
    else:
        form = RefundForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            mess = form.save(commit=False)
            #mess.student = Student.objects.get(user=request.user)
	    usr=User.objects.get(username=request.user.username)
	    stud=Student()
	    stud=Student.objects.get(user=usr)
			
			

        		
            			
            from_date=request.POST.get('from_date')
	    to_date=request.POST.get('to_date')
				
	    messrefund=Refund()
	    messrefund.from_date=from_date
	    messrefund.mail_proof=request.FILES.get('mail_proof')
	    messrefund.to_date=to_date
	    messrefund.student=stud
           
            #mess.mail_proof = request.FILES['mail_proof']
            file_type = mess.mail_proof.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    #'mess': mess,
                    #'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'Mess/messrefund.html', context)
            messrefund.save()
            return render(request, 'Mess/messrefund.html', {'error_message': 'refund form submitted successfully'})
        context = {
            "form": form,
        }
        return render(request, 'Mess/messrefund.html', context)


def feedback(request):
    if not request.user.is_authenticated():
        return render(request, 'Mess/login.html')
    else:
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            mess = form.save(commit=False)
            mess.student = Student.objects.get(user=request.user)
            mess.save()
            return render(request, 'Mess/popup.html', {'error_message': 'feedback submitted successfully'})
        context = {
            "form": form
        }
        return render(request, 'Mess/messcomplaint.html', context)
def messmanagerfeedback(request):
	k=len(MessFeedback.objects.all())
	mess_Complaint=[]
	student=[]
	complain_time=[]
	MessFeedback_data=MessFeedback.objects.all().order_by('time')
	
	room_regis=RoomRegistration.objects.all()
	m=len(RoomRegistration.objects.all())
	l=0
	for i in MessFeedback_data:
		for j in room_regis:
			if(i.student==j.student):
				
				mess_Complaint.append(str(i.student))
				mess_Complaint.append(str(i.feedback))
				mess_Complaint.append(str(i.time))
				mess_Complaint.append(str(j.pref_room_no))
				mess_Complaint.append(str(j.hostel_name))
				
			
	MessFeedback_data=MessFeedback.objects.all().order_by('time')
	
	listoflist=[]
	for row in range(len(mess_Complaint)/5):
		innerlist=[]
		for col in range(5):
			innerlist.append(mess_Complaint[row*5+col])
		listoflist.append(innerlist)
	print(listoflist)
	
	context2={'mess_complaint':listoflist}
	return render(request,'Mess/messmanagerfeedback.html',context2)
	


