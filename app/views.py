"""
Definition of views.
"""

from datetime import datetime, date
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.views.generic import View
from .forms import WishForm, UserForm
from .models import User, Wish
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
import bcrypt

def home(request):
    if 'userid' in request.session:
        assert isinstance(request, HttpRequest)
        mywishes = Wish.objects.filter(user=request.session["userid"], granted=not True)
        grantedwishes = Wish.objects.filter(granted = True)
        return render(
            request,
            'app/dashboard.html',
            {
                'title':'Wishes',
                'mywishes':mywishes,
                'grantedwishes':grantedwishes
            }
        )
    else:
        return render(
            request, 
            'app/index.html',
            {
                'title':'Welcome! Sign in to make a wish!',
            }
        )

# **************** WISH

class Wish_View(View):
    def get(self, request, id):
        if 'userid' not in request.session:
            return redirect("/")
        wish = Wish.objects.get(id=id)
        print(wish)
        form = WishForm(instance = wish)
        context = {
           'title':"Let's edit your wish!",
           'action':'/wishes/edit/' + str(id) + "/",
           "regForm": form
          }
        return render(request, 'app/form.html', context)
    def post(self, request, id):
        if 'userid' not in request.session:
            return redirect("/")
        wish = Wish.objects.get(id=id)
        form = WishForm(request.POST,instance=wish)
        if form.is_valid():
            form.save()
        return redirect('/')

def wish_remove(request, id):
    if 'userid' not in request.session:
        return redirect("/")
    Wish.objects.filter(id=id).delete()
    return redirect('/')

def wish_like(request, id):
    if 'userid' not in request.session:
        return redirect("/")
    wish = Wish.objects.get(id=id)
    if 'wish' + str(id) not in request.session:
        wish.likes = wish.likes + 1
        wish.save()
        request.session['wish' + str(id)] = 'wish' + str(id)
    return redirect('/')

def wish_granted(request, id):
    if 'userid' not in request.session:
        return redirect("/")
    wish = Wish.objects.get(id=id)
    wish.granted = True
    wish.save()
    return redirect('/')

def wish_stats(request):
    if 'userid' not in request.session:
        return redirect("/")
    assert isinstance(request, HttpRequest)
    all_granted_wishes = Wish.objects.filter(granted=True).count()
    your_granted_wishes = Wish.objects.filter(user=request.session["userid"], granted=True).count()
    your_pending_wishes = Wish.objects.filter(user=request.session["userid"], granted=False).count()
    return render(
        request,
        'app/stats.html',
        {
            'title':'These are your stats!',
            'all_granted_wishes':all_granted_wishes,
            'your_granted_wishes':your_granted_wishes,
            'your_pending_wishes':your_pending_wishes
        }
    )

def wish_new(request):
    if 'userid' not in request.session:
        return redirect("/")
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/create/')
    title = request.POST['title']
    description = request.POST['description']
    user = User.objects.get(id = request.session['userid'])
    likes = 0
    granted = False
    wish = Wish.objects.create(title = title, description = description, user = user, likes = likes, granted = False)

    #form = WishForm(request.POST)
    #if form.is_valid():
    #    print(form)
    #    print(form.save())
    return redirect('/')

def wish_create(request):
    if 'userid' not in request.session:
        return redirect("/")
    form = WishForm
    context = {
        'title':"Make a wish!",
        'action':'/wishes/new/',
        'regForm':form,
        }
    return render(request, 'app/form.html', context)

# **************** TYPE

#def type(request):
#    if 'userid' not in request.session:
#        return redirect("/")
#    assert isinstance(request, HttpRequest)
#    logged_user = User.objects.get(id=request.session["userid"])
#    context = {
#            'title':'Types',
#            'name':logged_user,
#            'types':Type.objects.all()
#        }
#    return render(request, 'app/types.html', context)


#class Type_View(View):
#    def get(self, request, id):
#        if 'userid' not in request.session:
#            return redirect("/")
#        type = Type.objects.get(id=id)
#        print(type)
#        form = TypesForm(instance = job)
#        context = {
#           'title':'Edit Type',
#           'action':'/type/edit/' + str(id),
#           "regForm": form
#          }
#        return render(request, 'app/form.html', context)
#    def post(self, request, id):
#        if 'userid' not in request.session:
#            return redirect("/")
#        type = Type.objects.get(id=id)
#        form = TypesForm(request.POST,instance=job)
#        if form.is_valid():
#            form.save()
#        return redirect('/')

#def type_remove(request, id):
#    Type.objects.filter(id=id).delete()
#    return redirect('/')

#def type_new(request):
#    if 'userid' not in request.session:
#        return redirect("/")
#    errors = Type.objects.type_validator(request.POST)
#    if len(errors) > 0:
#        for key, value in errors.items():
#            messages.error(request, value)
#        return redirect('/types')
#    title = request.POST['title']
#    type = Type.objects.create(title = title)
#    print (type)
#    return redirect('/')

#def type_create(request):
#    if 'userid' not in request.session:
#        return redirect("/")
#    form = TypesForm
#    logged_user = User.objects.get(id=request.session["userid"])
#    context = {
#        'title':'Create a job!',
#        'name':logged_user,
#        'action':'/type/new/',
#        'regForm':form,
#        }
#    return render(request, 'app/form.html', context)


# *************** LOGIN / REGISTRATION

def register(request):

    first_name = request.POST["p_fname"]
    last_name = request.POST["p_lname"]
    email = request.POST["p_email"]
    password = request.POST["p_pword"]
    confirm = request.POST["p_confirm"]

    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    encrypted_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print(encrypted_pw)
    m_user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = encrypted_pw)
    print(m_user.password)
    return redirect("/")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email = request.POST["login-email"]
        user = User.objects.get(email=email)
        full_name = user.first_name + " " + user.last_name
        print(user.__dict__)
        request.session["userid"] = user.id
        request.session["first_name"] = user.first_name
        request.session["last_name"] = user.last_name
        request.session["full_name"] = full_name
        return redirect("/")

def logout(request):
    if 'userid' not in request.session:
        return redirect("/")
    request.session.flush()
    return redirect("/")
