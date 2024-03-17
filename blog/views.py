from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


@login_required(login_url="/login")
def create_blog(request):
    if request.method == "POST":
        data = request.POST

        title = data.get("title")
        content = data.get("content")
        image = request.FILES.get("image")

        user = request.user

        Blog.objects.create(title=title, content=content, image=image, user=user)

        return redirect("/")

    return render(request, "create.html")


@login_required(login_url="/login")
def delete_blog(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except ValueError:
        raise Http404("Invalid blog ID")

    if request.user != blog.user:
        return HttpResponseForbidden("You do not have permission to delete this blog.")

    blog.delete()
    return redirect("/")


@login_required(login_url="/login")
def update_blog(request, id):

    try:
        blog = Blog.objects.get(id=id)
    except:
        return redirect("/")

    if request.method == "POST":

        if request.user != blog.user:
            return HttpResponseForbidden(
                "You do not have permission to update this blog."
            )

        data = request.POST
        title = data.get("title")
        content = data.get("content")
        image = request.FILES.get("image")

        if title:
            blog.title = title
        if content:
            blog.content = content
        if image:
            blog.image = image

        blog.save()

        return redirect("/")

    elif request.user == blog.user:
        return render(request, "update.html", context={"blog": blog})

    else:
        return redirect("/")


def each_blog(request, id):
    try:
        blog = Blog.objects.get(id=id)
        new_count = blog.view_count + 1
        blog.view_count = new_count
        blog.save()
    except:
        return redirect("/")
    return render(request, "blog.html", context={"blog": blog})
