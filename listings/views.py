from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from .models import Message
from .forms import MessageForm


def item_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Display all items to admin
        items = Item.objects.all()
    else:
        # Display only approved items to regular users
        items = Item.objects.filter(approved=True)

        # Add a new context variable indicating whether each item belongs to the current user
    for item in items:
        item.is_owner = item.owner == request.user if request.user.is_authenticated else False

        # Handle county filtering if a county is selected
    county_filter = request.GET.get('county')
    if county_filter:
        items = items.filter(county=county_filter)


     # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(items, 10)  # Show 10 items per page

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results
        items = paginator.page(paginator.num_pages)

    return render(request, 'listings/item_list.html', {'items': items})


def post_item(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the user is a normal user and has already created two posts
        if not request.user.is_staff and Item.objects.filter(owner=request.user).count() >= 2:
            # Redirect or display an error message to the user
            return render(request, 'listings/post_item_limit_reached.html')

        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.owner = request.user
                item.approved = request.user.is_staff
                item.save()

                # Add a success message
                messages.success(request, 'Post created successfully!')

                return  redirect('item_list')
        else:
            form = ItemForm()

        return render(request, 'listings/post_item.html', {'form': form})
    else:
        # Redirect to login page or display an error message for unauthenticated users
        return redirect('login')


def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Ensure that only the owner can edit their item
    if item.owner != request.user:
        return redirect('item_list')

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)

    return render(request, 'listings/edit_item.html', {'form': form, 'item': item})


def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Ensure that only the owner can delete their item
    if item.owner != request.user:
        return redirect('item_list')

    if request.method == 'POST':
        item.delete()
        return redirect('item_list')

    return render(request, 'listings/delete_item.html', {'item': item})


def read_more(request, pk):
    item = get_object_or_404(Item, pk=pk)

     # Check if the user is authenticated
    if request.user.is_authenticated:
     return render(request, 'listings/read_more.html', {'item': item})
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect('login')  # You need to import redirect from django.shortcuts


def send_message(request, recipient_id):
    recipient = User.objects.get(pk=recipient_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('inbox')  # Redirect to the inbox after sending the message
    else:
        form = MessageForm()

    return render(request, 'messages/send_message.html', {'form': form, 'recipient': recipient})


@login_required
def inbox(request):
    received_messages = request.user.received_messages.all()
    return render(request, 'messages/inbox.html', {'received_messages': received_messages})


def user_profile(request, username):
    owner = get_object_or_404(User, username=username)
    return render(request, 'user_profile.html', {'owner': owner})


def business_items(request):
    # Retrieve all items with type 'business'
    items = Item.objects.filter(type='business')
    return render(request, 'listings/business_items.html', {'items': items})


def business_items(request):
    # Retrieve all items with type 'business'
    items = Item.objects.filter(type='business')

    # Handle county filtering if a county is selected
    county_filter = request.GET.get('county')
    if county_filter:
        items = items.filter(county=county_filter)

    return render(request, 'listings/business_items.html', {'items': items})
