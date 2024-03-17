from django.shortcuts import render
from blog.models import *


def home(request):

    blogs = Blog.objects.all()

    # Apply filtering if search_query parameter is provided
    search_query = request.GET.get("search_query")
    if search_query:
        blogs = Blog.objects.filter(title__icontains=search_query)

    blogs = blogs.order_by("-view_count")[0:10]

    return render(
        request,
        "index.html",
        context={"blogs": blogs, "search_query": search_query},
    )
