from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext


@csrf_protect
def login(request):
    template = loader.get_template('Delta_HW/login.html')
    context = {}
    return HttpResponse(template.render(context, request))


# @csrf_protect
def index(request):
    un = request.POST["user_id"]
    pw = request.POST["password"]
    cp = Appuser.objects.all().filter(scur=un).values('password')[0]['password']
    u = Appuser.objects.get(scur=un)
    # cp = tmp['password']
    # fl = tmp['consecutive_failed_logins']
    if cp == pw:
        template = loader.get_template('Delta_HW/index.html', )
        context = {"current_user" : u}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('Delta_HW/login.html', )
        context = {"user": u, "fail": 1}
        return HttpResponse(template.render(context, request))
#
#
# @csrf_protect
# def createAppuser(request):
#     template = loader.get_template('Delta_HW/createAppuser.html', )
#     context = {}
#     return HttpResponse(template.render(context, request))
#
#
# @csrf_protect
# def userCreated(request):
#     if request.POST:
#         fn = request.POST["first_name"].upper()
#         ln = request.POST["last_name"].upper()
#         pw = request.POST["password"]
#         # sc = fn[0] + ln[0:3]
#         # cn = Appuser.objects.filter(scur__startswith=sc).count()
#         # if cn:
#         #     sc += str(cn + 1)
#         au = Appuser.create(fn, ln, pw)
#         # au.scur = sc
#         # au.user_first_name = fn
#         # au.user_last_name = ln
#         # au.password = pw
#         au.save()
#
#     template = loader.get_template('Delta_HW/users.html', )
#     users = Appuser.objects.order_by('user_first_name','user_last_name','scur')
#     context = {"users": users}
#     return HttpResponse(template.render(context, request))
#
#
# @csrf_protect
# def createP(request):
#     template = loader.get_template('Delta_HW/createPatient.html', )
#     context = {}
#     return HttpResponse(template.render(context, request))
#
#
# @csrf_protect
# def searchP(request):
#     template = loader.get_template('Delta_HW/searchPatient.html', )
#     context = {}
#     return HttpResponse(template.render(context, request))
#
#
# @csrf_protect
# def listP(request):
#     fn = request.POST["first_name"]
#     ln = request.POST["last_name"]
#     pts = Patient.objects.all().filter(first_name__icontains=fn, last_name__icontains=ln)
#
#     template = loader.get_template('Delta_HW/listPatient.html', )
#     context = {"pts": pts, "first_name": fn, "last_name": ln}
#     return HttpResponse(template.render(context, request))
#
#
# @csrf_protect
# def updatePatient(request):
#     if "paaa_id" in request.POST:
#         p = Patient.objects.get(paaa_id=request.POST["paaa_id"])
#         pa = Patient_Address.objects.get(paaa_id=p)
#     else:
#         p = Patient()
#         pa = Patient_Address()
#
#     p.first_name = request.POST["first_name"]
#     p.last_name = request.POST["last_name"]
#     p.gender = request.POST["gender"]
#     p.create_datetime = timezone.now()
#     p.create_userid = None
#     p.last_update_datetime = timezone.now()
#     p.last_update_userid = None
#
#     p.save()
#
#     pa.paaa_id = p
#     pa.primary_ph_no = request.POST["ph_no"]
#     pa.line_one = request.POST["add_1"]
#     pa.line_two = request.POST["add_2"]
#     pa.city = request.POST["city"]
#     pa.area_code = request.POST["areacode"]
#
#     pa.save()
#
#     template = loader.get_template('Delta_HW/updatePatient.html')
#     context = {'pat': p, 'padd': pa,}
#     return HttpResponse(template.render(context, request))
