from django.shortcuts import render, HttpResponse
from .models import Post,BlogComment
# Create your views here.
def blogHome(request):
    allposts=Post.objects.all()
    context={"allposts":allposts}
    return render(request,"blog/bloghome.html",context)



def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        comment = BlogComment(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")

    return redirect(f"/blog/{post.slug}")

def blogPost(request,slug):
    post = Post.objects.all(slug=slug)
    print(post)
    context1 = {"post": post,'comment': comment,'user':request.user}
    return render(request, "blog/blogpost.html", context1)
