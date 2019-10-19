from django.shortcuts import render

def Index_view(request):
    '''
    This is the function based view for the homepage
    '''
    title = "home"
    context = {
        "title":title
    }
    
    return render(request,"main/index.html",context)
