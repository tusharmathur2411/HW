from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader, RequestContext
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import datetime
from .forms import PatientForm, PatientAddressForm


@csrf_protect
def index(request):
    if request.session.get('user'):
        print('User already logged in: ' + request.session['user'])
        template = loader.get_template('Delta_HW/index.html', )
        global user
        user = Appuser.objects.get(scur=request.session['user'])
        context = {"current_user": user}
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        un = request.POST["user_id"]
        pw = request.POST["password"]
        cp = Appuser.objects.all().filter(scur=un).values('password')[0]['password']
        u = Appuser.objects.get(scur=un)
        print('Logging in user: ' + u.scur)
        if cp == pw:
            u.consecutive_failed_logins = 0
            u.save()
            request.session['user'] = u.scur
            template = loader.get_template('Delta_HW/index.html', )
            context = {"current_user" : u}
            return HttpResponse(template.render(context, request))
        else:
            u.consecutive_failed_logins += 1
            u.save()
            template = loader.get_template('Delta_HW/login.html', )
            context = {"user": u, "fail": u.consecutive_failed_logins}
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('Delta_HW/login.html')
        context = {}
        return HttpResponse(template.render(context, request))


@csrf_protect
def logout(request):
    print('Logging out user: ' + request.session['user'])
    request.session['user'] = None
    return HttpResponseRedirect(reverse('Delta_HW:index'))


@csrf_protect
def users(request):
    if request.session.get('user') is None:
        return HttpResponseRedirect(reverse('Delta_HW:index'))
    template = loader.get_template('Delta_HW/userList.html', )
    users = Appuser.objects.order_by('user_first_name', 'user_last_name', 'scur')
    context = {"users": users, "current_user": user}
    return HttpResponse(template.render(context, request))



@csrf_protect
def createAppuser(request):
    if request.session.get('user') is None:
        return HttpResponseRedirect(reverse('Delta_HW:index'))
    template = loader.get_template('Delta_HW/createAppuser.html', )
    context = {"current_user": user}
    return HttpResponse(template.render(context, request))


@csrf_protect
def userCreated(request):
    if request.session.get('user') is None:
        return HttpResponseRedirect(reverse('Delta_HW:index'))
    if request.POST:
        fn = request.POST["first_name"].upper()
        ln = request.POST["last_name"].upper()
        pw1 = request.POST["password1"]
        pw2 = request.POST["password2"]
        if pw1 == pw2:
            au = Appuser()
            au = au.create(fn, ln, pw1)
            au.save()
            return HttpResponseRedirect(reverse('Delta_HW:users'))
        else:
            return HttpResponseRedirect(reverse('Delta_HW:create_user'))
        # sc = fn[0] + ln[0:3]
        # cn = Appuser.objects.filter(scur__startswith=sc).count()
        # if cn:
        #     sc += str(cn + 1)
        # au = Appuser.create(fn, ln, pw)
        # au.scur = sc
        # au.user_first_name = fn
        # au.user_last_name = ln
        # au.password = pw
        # au.save()

    # template = loader.get_template('Delta_HW/userList.html', )
    # users = Appuser.objects.order_by('user_first_name','user_last_name','scur')
    # context = {"users": users}
    # return HttpResponse(template.render(context, request))
    # return HttpResponseRedirect(reverse('Delta_HW:users'))
#
#
# @csrf_protect
# def createP(request):
#     template = loader.get_template('Delta_HW/createPatient.html', )
#     context = {}
#     return HttpResponse(template.render(context, request))


@csrf_protect
def search_patients(request):
    if request.session.get('user') is None:
        return HttpResponseRedirect(reverse('Delta_HW:index'))
    context = {"current_user": user}
    if request.POST:
        fn = request.POST["first_name"]
        ln = request.POST["last_name"]
        pts = Patient.objects.all().filter(first_name__icontains=fn, last_name__icontains=ln)
        context = {"patients": pts, "first_name": fn, "last_name": ln, "current_user": user}
    template = loader.get_template('Delta_HW/searchPatient.html', )
    return HttpResponse(template.render(context, request))


@csrf_protect
def viewPatient(request):
    if request.session.get('user') is None:
        return HttpResponseRedirect(reverse('Delta_HW:index'))
    if request.POST.get("paaa_id"):
        new_patient = Patient.objects.get(paaa_id=request.POST.get("paaa_id"))
        new_address = PatientAddress.objects.get(paaa_id=new_patient)
    else:
        p = PatientForm(request.POST)
        pa = PatientAddressForm(request.POST)
        if p.is_valid() and pa.is_valid():
            new_patient = p.save(commit=False)
            new_address = pa.save(commit=False)
            new_address.paaa_id = new_patient
            new_patient.save()
            new_address.save()
            print(new_patient.__dict__)
            print(new_address.__dict__)
        else:
            error = p.errors
    
    patient_form = PatientForm(instance=new_patient)
    address_form = PatientAddressForm(instance=new_address)

    template = loader.get_template('Delta_HW/viewPatient.html')
    context = {'patient_form': patient_form, 'address_form': address_form, "current_user": user, "patient" : new_patient}
    return HttpResponse(template.render(context, request))


def createPatient(request):
    patient_form = PatientForm()
    address_form = PatientAddressForm()
    template = loader.get_template('Delta_HW/createPatient.html')
    context = {'patient_form': patient_form, 'address_form': address_form, "current_user": user}
    return HttpResponse(template.render(context, request))