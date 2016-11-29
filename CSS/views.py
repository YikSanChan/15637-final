from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
# send email from within Django
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset, password_reset_confirm
from CSS.forms import *
from CSS.models import *
from django.db.models import Count, Sum
from pandas import DataFrame
from math import sqrt


def CF():
    dataset = {}

    def pearson_correlation(person1, person2):
        # To get both rated items
        both_rated = {}
        for item in dataset[person1]:
            if item in dataset[person2]:
                both_rated[item] = 1
        number_of_ratings = len(both_rated)
        # Checking for number of ratings in common
        if number_of_ratings == 0:
            return 0
        # Add up all the preferences of each user
        person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
        person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])
        # Sum up the squares of preferences of each user
        person1_square_preferences_sum = sum([pow(dataset[person1][item], 2) for item in both_rated])
        person2_square_preferences_sum = sum([pow(dataset[person2][item], 2) for item in both_rated])
        # Sum up the product value of both preferences for each item
        product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])
        # Calculate the pearson score
        numerator_value = product_sum_of_both_users - (
            person1_preferences_sum * person2_preferences_sum / number_of_ratings)
        denominator_value = sqrt(
            (person1_square_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (
                person2_square_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
        if denominator_value == 0:
            return 0
        else:
            r = float(numerator_value) / denominator_value
            return r

    def user_reommendations(person):
        # Gets recommendations for a person by using a weighted average of every other user's rankings
        totals = {}
        simSums = {}
        rankings_list = []
        for other in dataset:
            # don't compare me to myself
            if other == person:
                continue
            sim = pearson_correlation(person, other)
            # ignore scores of zero or lower
            if sim <= 0:
                continue
            for item in dataset[other]:
                # only score menu i haven't eaten
                if item not in dataset[person] or dataset[person][item] == 0:
                    # Similrity * score
                    totals.setdefault(item, 0)
                    totals[item] += float(dataset[other][item]) * sim
                    # sum of similarities
                    simSums.setdefault(item, 0)
                    simSums[item] += sim
                    # Create the normalized list
        rankings = [(total / simSums[item], item) for item, total in totals.items()]

        ratings = {}
        for item, total in totals.items():
            rate = total / simSums[item]
            ratings.update({item: rate})
            user = User.objects.get(id=person)
            menu = Menu.objects.get(id=item)
            newRating = RatingSummary.objects.create(user=user, menu=menu, rating=rate)
            newRating.save()

        recommendataions_list = [recommend_item for score, recommend_item in rankings]
        return recommendataions_list

    # reset the old rating result
    RatingSummary.objects.all().delete()
    for i in User.objects.all():
        OneUserData = {}
        userOrder = Order.objects.filter(customer=i.id)
        for u in userOrder:
            OneUserData.update({u.menu.id: u.rating})
            user = User.objects.get(id=i.id)
            menu = Menu.objects.get(id=u.menu.id)
            newRating = RatingSummary.objects.create(user=user, menu=menu, rating=u.rating)
            newRating.save()
        dataset.update({i.id: OneUserData})

    for i in User.objects.all():
        user_reommendations(i.id)


def daily():
    noCF = (len(RatingSummary.objects.all()) == 0)  # If no data in the RatingSummary databse, return home
    if (noCF):
        print("No historical rating data")
        return redirect(reverse('home'))
    query = Menu.get_today_menu()

    if timezone.localtime(timezone.now()).__lt__(datetime.datetime(2016, 11, 28, 12, tzinfo=datetime.timezone.utc)):
        today_lunch = Menu.get_today_lunch()
        query = Menu.get_today_lunch()
        print("today lunch: ", today_lunch)
    else:
        today_dinner = Menu.get_today_dinner()
        query = Menu.get_today_dinner()
        print("today dinner: ", today_dinner)

    dailyMenu = []
    for q in query:
        dailyMenu.append(Menu.objects.get(id=q.id))

    print("query", query)
    print("dailyMenu", dailyMenu)
    dailyRecommender = []

    for i in Profile.objects.filter(type=False):  # only recommend to mechant
        priority = []
        for d in dailyMenu:
            MenuList = Menu.objects.filter(food_name=d.food_name, meal_date__lte=datetime.date.today())
            # if the item never show up before, we score them lower
            ratingSum = 0
            if (len(MenuList) == 0):
                pair = (d.id, 0)
            else:
                for m in MenuList:
                    # print("menu", m.id, "user", i.user.id)
                    # print (RatingSummary.objects.filter(user=i.user, menu=m))
                    # print(RatingSummary.objects.get(user=i.user, menu=m))
                    # if len(RatingSummary.objects.get(user=i.user, menu=m))==0:
                    #     return redirect(reverse('home'))
                    # ratingSum += RatingSummary.objects.get(user=i.user, menu=m).rating
                    for r in RatingSummary.objects.filter(user=i.user, menu=m):
                        ratingSum += r.rating

                ratingAvg = ratingSum / len(MenuList)
                pair = (d.id, ratingAvg)
            priority.append(pair)

        def getKey(item):
            return item[1]  # sort by rating, not menu id

        sortedMenu = sorted(priority, key=getKey, reverse=True)
        print(i.user.id, "'s preference: ", sortedMenu)
        dailyRecommender.append((i.user.id, sortedMenu))
    print("recommender", dailyRecommender)
    return dailyRecommender


@transaction.atomic
def register(request):
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'CSS/register.html', {'form': form})
    new_user = form.save(commit=False)
    new_user.save()

    # activation from email
    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to Chinese Stomach Savior. Please click the link below to verify your email address
    and complete the registration of your account: http://%s%s
    """ % (request.get_host(), reverse('confirm_email', kwargs={'username': new_user.username, 'token': token}))
    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="yiksanc@andrew.cmu.edu",
              recipient_list=[new_user.email])
    context = {'email': form.cleaned_data['email']}
    return render(request, 'CSS/need_confirmation.html', context)


def confirm_registration(request, username, token):
    # Things happen after new user receive confirmation email,
    # and click the link.
    new_user = User.objects.filter(username=username)[0]
    new_user.is_active = True
    new_user.save()
    return redirect(reverse('login'))


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request,
                                  # template_name='grumblr/reset_confirm.html',
                                  uidb64=uidb64,
                                  token=token,
                                  post_reset_redirect=reverse('login'))


def reset(request):
    return password_reset(request,
                          # template_name='grumblr/reset.html',
                          # email_template_name='grumblr/reset_email.html',
                          # subject_template_name='grumblr/reset_subject.txt',
                          post_reset_redirect=reverse('login'))


@login_required
def home(request):
    # CF()
    # print(daily())
    profile_to_edit = get_object_or_404(Profile, user=request.user)
    if profile_to_edit.type is None:  # user type not yet stored in database
        # if type selected
        if 'type' in request.POST and request.POST['type'] is not None:
            form = UserTypeForm(request.POST, instance=profile_to_edit)
            form.save()
        # if type not yet selected
        else:
            return render(request, 'CSS/choose_user_type.html', {'form': UserTypeForm()})
    # home page
    all_menus = Menu.get_today_menu()
    # if all_menus is [], filter() throw error
    merchant_menus = all_menus.filter(merchant=request.user) if all_menus else {}
    if request.user.profile.type:  # merchant user
        data = merchant_order_statistics(request)
        return render(request, 'CSS/merchant_home.html',
                      {'profile': profile_to_edit, 'menus': merchant_menus, 'data': data})
    else:  # student user
        user_today_orders = Order.get_today_orders().filter(customer=request.user)
        user_today_orders_count = [(o, get_sum_by_id(o.menu_id)) for o in user_today_orders]
        ordered_menus = [order.menu for order in user_today_orders]
        unordered_menus = list(set(Menu.get_today_menu()) - set(ordered_menus))
        menu_form_list = [(menu, OrderQuantityForm(initial={'menu_id': menu.id}), get_sum_by_id(menu.id)) for menu in
                          unordered_menus]

        return render(request, 'CSS/student_home.html',
                      {'profile': profile_to_edit,
                       'user_today_orders': user_today_orders_count,
                       'unordered_menus': unordered_menus,
                       'unordered_menus_forms': menu_form_list})


@login_required
def browse_profile(request, profile_id):
    profile_to_browse = get_object_or_404(Profile, id=profile_id)
    return render(request, 'CSS/browse_profile.html',
                  {'profile': profile_to_browse, 'user_id': request.user.id, 'is_merchant': profile_to_browse.type})


@login_required
def edit_profile(request, profile_id):
    profile_to_edit = get_object_or_404(Profile, id=profile_id)
    if int(profile_id) != request.user.profile.id:
        return redirect(reverse('home'))
    if request.method == 'GET':
        form = EditProfileForm(instance=profile_to_edit)
        return render(request, 'CSS/edit_profile.html', {'form': form, 'profile': profile_to_edit})
    form = EditProfileForm(request.POST, request.FILES, instance=profile_to_edit)
    if not form.is_valid():
        return render(request, 'CSS/edit_profile.html', {'form': form})
    form.save()
    return render(request, 'CSS/browse_profile.html', {'profile': profile_to_edit})


@login_required
def create_menu(request):
    if request.method == 'GET':
        return render(request, 'CSS/create_menu.html', {'form': MenuForm(), 'user': request.user})
    # create a new menu object
    new_menu = Menu(merchant=request.user)
    form = MenuForm(request.POST, request.FILES, instance=new_menu, initial={'user_id': request.user.id})
    if not form.is_valid():
        return render(request, 'CSS/create_menu.html', {'form': form})
    new_menu.save()
    for location_id in request.POST.getlist('locations'):
        location_id = int(location_id)
        location = get_object_or_404(Location, id=location_id)
        new_menu.location_set.add(location)
    form.save()
    return redirect(reverse('home'))


@login_required
def browse_menu(request, merchant_id):
    merchant = get_object_or_404(User, id=merchant_id)
    profile_id = merchant.profile.id
    return render(request, 'CSS/browse_menu.html',
                  {'menus': Menu.get_menus(merchant), 'profile_id': profile_id, 'user_id': request.user.id,
                   'username': merchant.username})


@login_required
def edit_menu(request, menu_id):
    menu_to_edit = get_object_or_404(Menu, id=menu_id)
    if menu_to_edit.merchant_id != request.user.id:
        return redirect(reverse('home'))
    if request.method == 'GET':
        form = MenuForm(instance=menu_to_edit)
        return render(request, 'CSS/edit_menu.html', {'form': form, 'menu': menu_to_edit})
    previous_is_lunch = True if request.POST['menu_type'] == 'True' else False
    form = MenuForm(request.POST, request.FILES, instance=menu_to_edit,
                    initial={'user_id': request.user.id, 'from_edit': True, 'previous_is_lunch': previous_is_lunch})
    if not form.is_valid():
        return render(request, 'CSS/edit_menu.html', {'form': form, 'menu': menu_to_edit})
    form.save()
    return redirect(reverse('home'))


@login_required
def delete_menu(request, menu_id):
    menu_to_delete = get_object_or_404(Menu, id=menu_id)
    merchant_id = menu_to_delete.merchant_id
    menu_to_delete.delete()
    return redirect(reverse('browse_menu', kwargs={'merchant_id': merchant_id}))


@login_required
def create_order(request):
    if request.method == 'GET':
        return redirect(reverse('home'))
    menu_id = int(request.POST['menu_id'])
    menu = get_object_or_404(Menu, id=menu_id)
    new_order = Order.objects.create(menu=menu, customer=request.user)
    form = OrderQuantityForm(request.POST, instance=new_order)
    if not form.is_valid():
        return redirect(reverse('home'))
    form.save()
    return redirect(reverse('home'))


@login_required
def browse_order(request, customer_id):
    customer = get_object_or_404(User, id=customer_id)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'CSS/browse_order.html', {'orders': orders, 'username': customer.username})


@login_required
def edit_order(request, order_id):
    order_to_edit = get_object_or_404(Order, id=order_id)
    if order_to_edit.customer_id != request.user.id:
        return redirect(reverse('home'))
    if request.method == 'GET':
        form = OrderQuantityForm(instance=order_to_edit, initial={'menu_id': order_to_edit.menu_id})
        return render(request, 'CSS/edit_order.html', {'form': form, 'order': order_to_edit})
    form = OrderQuantityForm(request.POST, instance=order_to_edit, initial={'menu_id': order_to_edit.menu_id})
    if not form.is_valid():
        return render(request, 'CSS/edit_order.html', {'form': form, 'order': order_to_edit})
    form.save()
    return redirect(reverse('home'))


@login_required
def delete_order(request, order_id):
    order_to_delete = get_object_or_404(Order, id=order_id)
    order_to_delete.delete()
    return redirect(reverse('home'))


@login_required
def pickup_notification(request):
    # url = pyqrcode.create('http://chengdugourmet.com/')
    # url.svg('uca.svg', scale=4)

    # email_list = [o.customer.email for o in Order.objects.filter(is_taken=False)]
    email_list = ['evan.chanyiksan@gmail.com']
    email_body = """
        Thank you for choosing Chinese Stomach Savior. Please pickup your food box ASAP.
        """
    send_mail(subject="Please pickup your food box ASAP",
              message=email_body,
              from_email="yiksanc@andrew.cmu.edu",
              recipient_list=[email_list])
    # subject, from_email, to = 'hello', 'yiksanc@andrew.cmu.edu', 'evan.chanyiksan@gmail.com'
    # text_content = 'This is an important message.'
    # html_content = '<img src="uca.svg">'
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    return HttpResponse("Please pickup your food box ASAP")


@login_required
def exchange(request):
    if request.method == 'GET':
        return render(request, 'CSS/exchange.html', {'form': ExchangeForm()})

    menu_id = int(request.POST['menu'])
    menu = get_object_or_404(Menu, id=menu_id)

    new_exchange = Exchange.objects.create(menu=menu,
                                           user=request.user,
                                           quantity=request.POST['quantity'],
                                           is_seller=request.POST['is_seller'])
    new_exchange.save()

    Exchange.objects.annotate(count_bento=Count('quantity'))

    return redirect(reverse('home'))


@login_required
def dashboard(request):
    # Group in SQL --> annotate in Django
    form = Exchange.objects.values('menu', 'is_seller').annotate(SubTotal=Sum('quantity'))
    restaurant = []
    for menu in form:
        restaurant.append((Menu.objects.get(pk=menu['menu']), menu['SubTotal']))
    context = {'form': form, 'restaurant': restaurant}

    return render(request, 'CSS/dashboard.html', context)


@login_required
def order_review(request):
    if request.method == 'GET':
        unreviewed = Order.objects.filter(customer=request.user, rating=0)
        return render(request, 'CSS/review.html', {'unreviewed': unreviewed, 'form': ReviewForm()})

    order_id = int(request.POST['order_id'])
    order = get_object_or_404(Order, id=order_id)
    order.rating = int(request.POST['rating'])
    order.save()

    return HttpResponse("review done")


@login_required
def pickup_order(request, order_id):
    order_to_pickup = get_object_or_404(Order, id=order_id)
    if order_to_pickup.is_taken:
        return HttpResponse("Your order is already taken.")
    order_to_pickup.is_taken = True
    return redirect(reverse('home'))


@login_required
def add_location(request):
    if request.method == 'GET':
        return render(request, 'CSS/add_location.html', {'form': AddLocationForm()})
    form = AddLocationForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'CSS/add_location.html', {'form': form})
    form.save()
    return render(request, 'CSS/add_location.html', {'form': AddLocationForm()})


def merchant_order_statistics(request):
    """
    Return a DataFrame table to inform merchant of orders status.
    Before creating menu, no DataFrame is displayed.
    After creating menu, empty DataFrame is constructed.
    And populated after customers place their orders.
    """
    today_menus = Menu.get_today_menu().filter(merchant=request.user)
    if not today_menus:
        return None
    orders = Order.get_today_orders().filter(menu__merchant=request.user)
    if not orders:
        locations = [o['location__id'] for o in today_menus.values('location__id').distinct()]
        locations = [str(Location.objects.filter(id=location_id)[0]) for location_id in locations]
        menus = ['Lunch', 'Dinner']
        df = DataFrame(0, index=locations, columns=menus)
        return df
    locations = [o['location_id'] for o in orders.values('location_id').distinct()]
    menus = [o['menu_id'] for o in orders.values('menu_id').distinct()]
    df = DataFrame(0, index=locations, columns=menus)
    for d in orders.values('location_id', 'menu_id').annotate(Sum('quantity')):
        df.ix[d['location_id']][d['menu_id']] = d['quantity__sum']
    locations = [str(Location.objects.filter(id=location_id)[0]) for location_id in locations]
    menus = ['Lunch' if Menu.objects.filter(id=menu_id)[0].is_lunch else 'Dinner' for menu_id in menus]
    df.index = locations
    df.columns = menus
    return df


def get_sum_by_id(menu_id):
    """
    How many times did the menu been ordered today.
    """
    orders = Order.get_today_orders()
    count = orders.filter(menu__id=menu_id).aggregate(Sum('quantity'))['quantity__sum']
    return count if count else 0
