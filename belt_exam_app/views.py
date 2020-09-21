from django.shortcuts import render, redirect
from .models import User, UserManager, Wish, WishManager
from django.contrib import messages
import bcrypt
from datetime import datetime, date, timedelta 

def index(request):
    return render(request, 'index.html')

# This is the main wishes page 
def wishes_page(request):
    if 'logged_in_user_id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id = request.session['logged_in_user_id'])
        all_user_wishes = user.wishes.filter(granted = False)
        all_wishes = Wish.objects.filter(granted = True)
        context = {
            'logged_in_user': user,
            'all_user_wishes': all_user_wishes,
            'all_wishes': all_wishes
        }
        return render(request, 'wishes.html', context)

def edit_wish_page(request, id):
    if 'logged_in_user_id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id = request.session['logged_in_user_id'])
        wish = Wish.objects.get(id = id)
        context = {
            'logged_in_user': user,
            'wish': wish
        }
        return render(request, 'edit_wish.html', context)

def new_wish_page(request):
    if 'logged_in_user_id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id = request.session['logged_in_user_id'])
        context = {
            'logged_in_user': user
        }
        return render(request, 'new_wish.html', context)

def show_stats(request):
    if 'logged_in_user_id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id = request.session['logged_in_user_id'])
        all_wishes = Wish.objects.all()
        granted_wishes_for_user = Wish.objects.filter(user = user).filter(granted = True)
        pending_wishes_for_user = Wish.objects.filter(user = user).filter(granted = False)

        
        context = {
            'logged_in_user': user,
            'all_wishes': all_wishes,
            'granted_wishes': granted_wishes_for_user,
            'pending_wishes': pending_wishes_for_user
        }
        return render(request, 'stats.html', context)

def logout(request):
    del request.session['logged_in_user_id']
    return redirect("/")

# ===================================================================== Non View Routes ====================================================================================
    
def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors) > 0:
        # grab each error and have them ready for the view to display 
        for key, value in errors.items():
            messages.error(request, value)
        # return to the page that you were on, the login page and have the user try again
        return redirect('/')
    else:
    # see if the username provided exists in the database
        user = User.objects.filter(email=request.POST['email']) 
        if user: # note that we take advantage of truthiness here: an empty list will return false
            logged_user = user[0] 
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['logged_in_user_id'] = logged_user.id
                # never render on a post, always redirect!copy
                return redirect('/wishes')
        # if we didn't find anything in the database by searching by username or if the passwords don't match, 
        # redirect back to a safe route
        return redirect("/")
    
def register(request):
    errors = User.objects.register_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # return to the page that you were on, the login page and have the user try again
        return redirect('/')
    else:
        # register the user, store them in the database and do whatever else is needed for this project
        hashedPassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        formData = request.POST

        new_user = User.objects.create(
            first_name = formData['first_name'],
            last_name = formData['last_name'],
            email = formData['email'],
            password = hashedPassword
        )
        
        request.session['logged_in_user_id'] = new_user.id
        return redirect("/wishes")

def add_wish(request):
    errors = Wish.objects.wish_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # return to the page that you were on
        return redirect('/wishes/new')
    else:
        user = User.objects.get(id=request.session['logged_in_user_id'])
        Wish.objects.create(
            wish_name = request.POST['wish_name'],
            description = request.POST['description'],
            user = user,
            likes  = 0
        )
    return redirect('/wishes')

def edit_wish(request, id):
    errors = Wish.objects.wish_validator(request.POST)
    wish = Wish.objects.get(id = id)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # return to the page that you were on
        return redirect(f'/wishes/edit/{wish.id}')
    else:
        wish.wish_name = request.POST['wish_name']
        wish.description = request.POST['description']
        print(wish.wish_name)
        print(wish.description )
        wish.save()
        return redirect('/wishes')

def remove_wish(request, id):
    Wish.objects.get(id = id).delete()
    return redirect('/wishes')

def grant_wish(request, id):
    wish = Wish.objects.get(id = id)
    wish.granted = True
    
    # using yesterday's date is just for testing the grnated date to ensure that is works properly. 
    today = date.today() 
    print("Today is: ", today) 
    yesterday = today - timedelta(days = 1) 
    print("Yesterday was: ", yesterday) 
    wish.date_granted = yesterday
    
    wish.save()
    return redirect('/wishes')

def like_wish(request, id, user_id):
    user = User.objects.get(id = user_id)
    wish = Wish.objects.get(id = id)
    wish.likes = wish.likes + 1
    wish.liked_by.add(user)
    wish.save()
    return redirect('/wishes')
