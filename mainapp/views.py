from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from .forms import profileForm
from user.models import User
from django.http import HttpResponseRedirect
# Create your views here.
@login_required(login_url='/login/')
def index(request):
    user = request.user
    album = Album.objects.filter(user__exact=user)
    # album_id = []
    # for al in album:
    #     album_id.append(al.album_id)
    # print(album_id)
    follow_table = Following.objects.filter(user_following__exact=user,relation__exact=False)
    request_counting = 0
    for i in follow_table:
        if i.relation is False:
            request_counting = request_counting + 1

    context = {
        "request_counting":request_counting,
        "album":album,
        "follow_table":follow_table
    }
    return render(request,'index.html',context)

def others_profile(request,username=None):
    user = request.user
    user.pk = request.user.pk
    print(user)
    profile_user = get_object_or_404(User,username=username)
    print(profile_user.pk)
    following = Following.objects.filter(user__exact=user)
    context={}
    

    if profile_user.pk == user.pk:
        return redirect('/')
    else:
        
            
            
        follow_tab = Following.objects.filter(user__exact=profile_user,user_following__exact=user)
        mw_follow = Following.objects.filter(user__exact=user,user_following__exact=profile_user)
        print(follow_tab)
        for i in follow_tab:
            if i:
                print(i.user_following)
                print(i.relation)
                if (i.relation == True):
                    album = Album.objects.filter(user__exact=profile_user)
                
                    followers_count = 0
                    followers = Following.objects.filter(user_following=profile_user,relation=True)
                    for im in followers:
                        followers_count = followers_count + 1
                    following_count = 0
                    following = Following.objects.filter(user=profile_user,relation=True)
                    for im in following:
                        following_count = following_count + 1
                    album_count = 0
                    
                    for im in album:
                        album_count = album_count + 1

                    context = {
                    "follow_tab":follow_tab,
            "profile_user":profile_user,
            "followers_count":followers_count,
            "following_count":following_count,
            "album_count":album_count,
            "my_follow":mw_follow
                    }
                
                    return render(request,'ui1.html',context)

            

        followers_count = 0
        followers = Following.objects.filter(user_following=profile_user,relation=True)
        for im in followers:
            followers_count = followers_count + 1
        following_count = 0
        following = Following.objects.filter(user=profile_user,relation=True)
        for im in following:
            following_count = following_count + 1
        album_count = 0
        album = Album.objects.filter(user__exact=profile_user)
        for im in album:
            album_count = album_count + 1
        context = {
            "follow_tab":follow_tab,
            "profile_user":profile_user,
            "followers_count":followers_count,
            "following_count":following_count,
            "album_count":album_count,
            "my_follow":mw_follow
            }
    
        return render(request,'ui1.html',context)

def feed(request):
    user = request.user
    user_f= Following.objects.filter(user__exact=user,relation=True)
    feed = []
    for u in user_f:
        unif = u.user_following
        album_feed = Album.objects.filter(user__exact=unif)
        
        feed.append(album_feed)

    print(feed)
    context={
        "feed":feed,
    }
    return render(request,'follow_feed.html',context)

def search(request):
    if request.method =="POST":
        q = request.POST.get('msearch')

    
        print(q)
        profiles_search = User.objects.filter(username__icontains=q)
        for p in profiles_search:
            print(p.username)
        context={
            "p_search":profiles_search,
        }

        return render(request,'search.html',context)

def single(request,pk=None,title=None):
    album = get_object_or_404(Album,pk=pk)
    sub = sub_album.objects.filter(main_title__exact=album)
    
    context={
        "title":title,
        "sub":sub,
        "al_id":pk,
    }


    return render(request, 'single.html',context)


def add_sub_album(request,album_id=None):
    if request.method == 'POST':
        if 'delete' in request.POST:
            del_album = get_object_or_404(Album,pk=album_id)
            del_album.delete()
            return redirect('/')
        else:
            new_sub_album = sub_album()

            new_sub_album.sub_title = request.POST.get('sub_title')
            main_album = get_object_or_404(Album,pk=album_id)
            main_id = album_id
            new_sub_album.main_title = main_album
            
            images = request.FILES.get('images')
            new_sub_album.images = images
            content = images
            
            fs = FileSystemStorage()
            fs.save('User_' + str(new_sub_album.main_title.user)+"/" + str(new_sub_album.main_title.album_id)+"/"+images.name,images)
            
            new_sub_album.sub_description = request.POST.get('sub_description')        

            if new_sub_album.main_title.album_id is None:
                return render(request, 'add_sub_album.html')
            else:
                new_sub_album.save()
                if 'stop-add' in request.POST:
                    return redirect('/')
                else:
                    return redirect('add_sub_album',album_id=main_album.album_id)

    else:
        
        return render(request, 'add_sub_album.html')




@login_required(login_url='/login/')
def add_album(request):
    if request.method == 'POST':
        user = request.user
        
        
        new_album = Album()

        new_album.title = request.POST.get('title')
        new_album.user = user
        new_album.memory_date = request.POST.get('memory_date')
        new_album.description = request.POST.get('description')
        new_album.Album_cover_img = request.FILES.get('imagi')
        print(new_album.Album_cover_img)
        
        if  new_album.Album_cover_img:
            
        
            images = new_album.Album_cover_img
            fs = FileSystemStorage()
            fs.save('User_' + str(user)+"/" + 'album_cov_' + str(new_album.pk)+"/"+images.name,images)
        
        something = len(new_album.title)
        if something == 0 :
            messages.error(request,'please enter a title for your album to continue')
            return render(request, 'add_album.html')

        else:
            new_album.save()
            
            
            return redirect('add_sub_album',album_id=new_album.album_id)

    else:
        new_album = Album()
        return render(request, 'add_album.html')


def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        
        print(user)
        new_profile = Profile()

        
        new_profile.user = user
        print(new_profile.user)
        new_profile.bio = request.POST.get('bio')
        print(new_profile.bio)
        new_profile.name = request.POST.get('fname')
        print(new_profile.name)
        new_profile.gender = 3
        print(new_profile.gender)
        images = request.FILES.get('images')
        if images is None:
            new_profile.save()
            return redirect('/')
        else:


            new_profile.images = images
            content = images
        
            fs = FileSystemStorage()
            fs.save('User_' + str(user)+"/"+images.name,images)
            new_profile.save()
            return redirect('/')


    return render(request, 'edit.html')



def profile(request,id=None):
    if request.method == 'POST':
        user = request.user
        print(user)
        
        new_profile = Profile()

        
        new_profile.user = user
        print(new_profile.user)
        new_profile.bio = request.POST.get('bio')
        print(new_profile.bio)
        new_profile.name = request.POST.get('fname')
        print(new_profile.name)
        new_profile.gender = 3
        print(new_profile.gender)
        images = request.FILES.get('images')
        if images is None:
            new_profile.save()
            return redirect('/')
        else:


            new_profile.images = images
            content = images
        
            fs = FileSystemStorage()
            fs.save('User_' + str(user)+"/"+images.name,images)
            new_profile.save()
            return redirect('/')


    return render(request, 'edit.html')



    return render(request)

def follow_request(request,id=None):
    user = request.user
    print(user)
    user_following = get_object_or_404(User,id=id)#user that is following. me following others
    
    table_fol = Following.objects.filter(user__exact=user,user_following__exact=user_following)
    for i in table_fol:
        if i:
            print(i)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
    
    follow_tab = Following()
    follow_tab.user = user
    follow_tab.user_following = user_following
    follow_tab.relation = False

    follow_tab.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def follow_accept(request,id=None):
    user = request.user
    user_follower = get_object_or_404(User,id=id)
    
    table_fol = Following.objects.filter(user__exact=user_follower,user_following__exact=user)
    follow_req_accept = get_object_or_404(Following,user=user_follower,user_following=user)
    print(follow_req_accept)
    follow_req_accept.relation = True
    print('accepted')
    follow_req_accept.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def follow_del_or_rej(request,id=None):#unfollow also
    user = request.user
    del_tab = get_object_or_404(Following,user=user,user_following=id)
    print(del_tab)
    del_tab.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def block_user(request,b_id=None):
    user = request.user
    
    b_user= get_object_or_404(User,id=b_id)

    block_tab = Blocked()
    block_tab.user = user
    block_tab.user_following = user_following.pk

    block_tab.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def settings(request):
    
    return render(request,'settings.html')

def followers(request):
    user = request.user
    user_followers = Following.objects.filter(user_following__exact=user)
    context = {
        "user_followers":user_followers
    }
    return render(request,'followers.html',context)

def following(request):
    user = request.user
    user_following = Following.objects.filter(user__exact=user,relation=True)
    context = {
        "user_following":user_following
    }
    return render(request,'Following.html',context)

def liked(request):
    user = request.user
    liked_user = Likes.objects.filter(liked_user__exact=user)
    context = {
        "liked_user":liked_user
    }
    return render(request,'liked.html',context)

def saved(request):
    user = request.user
    user_saved = Saved.objects.filter(user_saved__exact=user)
    context = {
        "user_saved":user_saved
    }
    return render(request,'saved.html',context)

def delete(request):
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def show_album(request,id=None):
    user = request.user
    album_dis = get_object_or_404(Album,album_id=id)
    user_like = Likes.objects.filter(album_id__exact=id,liked_user=user)
    like_store = Likes.objects.filter(album_id__exact=id)
    user_bookmark = Saved.objects.filter(Saved_album__exact=id,user_saved=user)
    l_count = 0
    for l in like_store:
        l_count = l_count + 1
    comments_store = Comments.objects.filter(album_id__exact=id)
    c_count = 0
    for c in comments_store:
        c_count = c_count + 1
    context = {
        "album_dis":album_dis,
        "like_store":like_store,
        "user_like":user_like,
        "l_count":l_count,
        "user_bookmark":user_bookmark,
        "c_count":c_count,
        "comments_store":comments_store,
    }
    return render(request,'show_album.html',context)
def about_profile(request):
        return render(request,'about1.html')
def contact_profile(request):
        return render(request,'contact1.html')

def save_like(request,id=None):
    user = request.user
    like_store = Likes()
    like_store.album_id = get_object_or_404(Album,pk=id)
    like_store.liked_user = user
    like_store.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def un_like(request,id=None):
    user = request.user
    like_store = Likes.objects.filter(album_id__exact=id,liked_user=user)
    
    like_store.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def bookmark(request,id=None):
    user = request.user
    bookmark_store = Saved()
    bookmark_store.Saved_album = get_object_or_404(Album,pk=id)
    bookmark_store.user_saved = user
    bookmark_store.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def del_bookmark(request,id=None):
    user = request.user
    bookmark_store = Saved.objects.filter(Saved_album__exact=id,user_saved=user)
    bookmark_store.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_comments(request,id=None):
    user = request.user
    if request.method == 'POST':
        add_com = Comments()
        add_com.album_id = get_object_or_404(Album,pk=id)
        add_com.comment_text = request.POST.get('comment-sav')
        add_com.comment_user = user
        add_com.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

