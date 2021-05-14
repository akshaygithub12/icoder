from django.shortcuts import render, HttpResponse,redirect
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from blog.models import Post

# Create your views here.
def home(request):
    return render(request,"home/home.html")

def contact(request):
    messages.success(request,"welcome to contact")
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<3:
            messages.error(request,"please fill data properly")
        else:
            contact1=Contact(name=name, email=email, phone=phone, content=content)
            contact1.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 - Not found")

def handeLogin(request):
    if request.method == "POST":
            # Get the post parameters
            loginusername = request.POST['loginusername']
            loginpassword = request.POST['loginpassword']

            user = authenticate(username=loginusername, password=loginpassword)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials! Please try again")
                return redirect("home")

    return HttpResponse("404- Not found")

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def about(request):
    return render(request, "home/about.html")

def search(request):
    query=request.GET["query"]
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsauthor = Post.objects.filter(author__icontains=query)
        allPostscontent = Post.objects.filter(content__icontains=query)
        # allPosts=Post.objects.all()
        allPosts= allPostsTitle.union(allPostsauthor,allPostscontent)
    if allPosts.count()==0:
        messages.warning(request,"no search result found")
    params = {"allPosts": allPosts,'query':query}
    return render(request, "home/search.html", params)
#    return HttpResponse("this is the one")