from django.shortcuts import render

# Create your views here.
def home(request):
    blogs = {
        'title':'test_title',
        'body': 'test_body'
    }
    return render(request, "blogs/blog_home.html", {"blogs": blogs})

