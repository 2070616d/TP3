# -*- coding: iso-8859-1 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import auth
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from stove.models import *
from stove.forms import *
from datetime import date
try:
    from django.utils import simplejson as json
except ImportError:
    import json


def index(request):
    """
    Index page view, shown only to non-logged in users.
    Has login and registration forms.
    """

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('userProfile'))

    # Render the template depending on the context.
    return render(request,
                  'index.html',
                  {'request': request, 'user_form': UserForm(), 'profile_form': UserProfileForm(), 'login_form': LoginForm()})


@require_POST
def registrationview(request):
    """Visitors get sent here temporarily when registering."""

    errors = {}
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileFormRegister(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit = False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            auth.login(request, auth.authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password']))
            return HttpResponseRedirect(reverse('userProfile'))
        else:
            # something went wrong? pass it on for rendering
            errors['user1'] = user_form.errors
            errors['user2'] = profile_form.errors
    return render(request, 'index.html', {'errors': errors, 'user_form': UserForm(), 'profile_form': UserProfileForm(), 'login_form': LoginForm()})


@login_required
def socialLoginFinalise(request):
    """Visitors get sent here to enter their details when they log in using social networks."""

    # Render the template depending on the context.
    return render(request,
                  'stove/socialLoginFinalise.html',
                  {'profile_form': UserProfileForm()})


@login_required
@require_POST
def registrationviewSocial(request):
    """
    This view processes details into UserProfile entities.
    Visitors get sent here temporarily when registering with social networks.
    """

    errors = None
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('socialLoginFinalise'))

    profile_form = UserProfileFormRegister(data=request.POST)

    # If the forms is valid...
    if profile_form.is_valid():
        # Now sort out the UserProfile instance.
        # Since we need to set the user attribute ourselves, we set commit = False.
        # This delays saving the model until we're ready to avoid integrity problems.
        profile = profile_form.save(commit=False)
        profile.user = request.user

        # Now we save the UserProfile model instance.
        profile.save()
        return HttpResponseRedirect(reverse('userProfile'))

    # something went wrong? pass it on for rendering
    errors = profile_form.errors
    return render(request, 'stove/socialLoginFinalise.html', {'errors': errors, 'profile_form': UserProfileForm()})


def loginview(request):
    """Visitors get sent here temporarily when logging in."""

    errors = {}
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if not (login_form.is_valid()):
            # Invalid form or forms - mistakes or something else?
            # They'll also be shown to the user.
            errors['login'] = "Please provide your username & password."
        else:
            user = auth.authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                if not login_form.cleaned_data['remember']:
                        request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('userProfile'))
            else:
                # something went wrong? pass it on for rendering
                errors['login'] = "Incorrect username and/or password."
    return render(request, 'index.html', {'errors': errors, 'user_form': UserForm(), 'profile_form': UserProfileForm(), 'login_form': LoginForm()})


@login_required
def preferences(request):
    """
    Edit preferences view.
    Really a formset with a whole bunch of tick boxes.
    """

    context_dict = {}
    preferences_list = Preference.objects.all()
    sub_preferences_nonnumbered_list = SubPreference.objects.all()

    # because of subpreferences (two-tiered system) and all that jazz we need to have a NUMBERED LIST that's an array

    # WHY ARE WE DOING THIS? when we get subpreferences as a list via .all(), they won't necessarily be ordered by their respective preference
    # but rather by order of input to DB. Therefore we need to enforce orderedness to make sure the view & the data structures are coherent

    # this also helps with javascript widgets that tick/untick all boxes of the same category

    # the following algorithms operate on this premise and could probably be made more concise. tread with care

    sub_preferences_list = []
    prefFormSet = formset_factory(PrefCheckbox, extra=len(sub_preferences_nonnumbered_list))
    count = 0
    # if it's a POST, i.e. someone is updating their data....
    if request.method == 'POST':
        formset = prefFormSet(request.POST)
        # update (i.e. re-input) their preferences as told
        for form in formset:
            if form.is_valid() and form.cleaned_data == {}:
                UserPreference.objects.filter(preference=sub_preferences_nonnumbered_list[count], user=request.user).delete()
            else:
                UserPreference.objects.get_or_create(preference=sub_preferences_nonnumbered_list[count], user=request.user)
            count = count + 1
        return userProfile(request)

    # Now that we're done with any possible POSTs, build (or rebuild) the formset with the correct preferences data.
    count = 0
    formset = prefFormSet()
    for sp in sub_preferences_nonnumbered_list:
        checked = UserPreference.objects.filter(preference=sp, user=request.user).exists()
        if checked:
            checked = "checked"
        else:
            checked = ""
        sub_preferences_list += [{'sp': sp, 'number': count, 'checked': checked}]
        count = count + 1
    context_dict = {'preferences_list': preferences_list, 'sub_preferences_list': sub_preferences_list, 'formset': formset}
    return render(request, 'stove/preferences.html', context_dict)


@login_required
def userProfile(request):
    """
    User profile view.
    Basically operates by passing down a bunch of objects to the template. That's all there is to it, really.
    """

    context_dict = {}
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('socialLoginFinalise'))

    # Certain options (like changing passwords) are unavailable to social login users, because that would be silly
    sociallogin = False
    try:
        sociallogin = request.user.social_auth.get()
    except ObjectDoesNotExist:
        pass

    # now pull a lot of user data, which we later pass on to the front-end for rendering
    user_event = EventAttendance.objects.filter(user=request.user)
    event_list = Event.objects.all()
    sub_preferences_list = []
    preferences_list = Preference.objects.all()
    sub_preferences_nonnumbered_list = SubPreference.objects.all()
    count = 0
    for sp in sub_preferences_nonnumbered_list:
        # this annoying chunk of code deals with the nice preferences visualisation
        checked = UserPreference.objects.filter(preference=sp, user=request.user).exists()
        if checked:
            checked = True
        else:
            checked = False
        sub_preferences_list += [{'sp': sp, 'number': count, 'checked': checked}]
        count = count + 1

    context_dict = {'user_event': user_event,
                    'sociallogin': sociallogin,
                    'UserProfile': user_profile,
                    'preferences_list': preferences_list, 'sub_preferences_list': sub_preferences_list,
                    'event_list': event_list}
    return render(request, 'stove/userProfile.html', context_dict)


def cafe(request):
    """
    Cafe menu view.
    Basically operates by passing down a bunch of objects and related metrics to the template. That's all there is to it, really.
    """

    context_dict = {}
    try:
        cafe_categories = CafeCategory.objects.all()
        items = CafeItem.objects.all()
        cafe_items = []
        for item in items:
            meLikey = False
            if request.user.is_authenticated():
                meLikey = CafeItemLike.objects.filter(item=item, user=request.user).exists()
            cafe_items += [{'item': item, 'numLikes': len(CafeItemLike.objects.filter(item=item)), 'meLikey': meLikey}]
        context_dict = {'cafe_categories': cafe_categories, 'cafe_items': cafe_items}
    except:
        pass
    return render(request, 'stove/cafe.html', context_dict)


@login_required
@require_POST
def cafeItemLike(request):
    """POST -> JSON view that allows users to like/unlike cafe items"""

    ctx = {}
    pk = request.POST.get('pk', None)
    try:
        item = CafeItem.objects.get(pk=pk)
    except:
        return

    try:
        # if the like exists, delete it and tell the front-end that we're not liking it anymore
        like = CafeItemLike.objects.get(user=request.user, item=item)
        like.delete()
        ctx['meLikey'] = False
    except:
        # if there's an exception (the like doesn't exist), create a like and tell the front-end that we're liking it
        CafeItemLike.objects.get_or_create(user=request.user, item=item)
        ctx['meLikey'] = True

    # pass the front-end an updated number of likes, because otherwise it gets reeeeal messy.
    ctx['numLikes'] = len(CafeItemLike.objects.filter(item=item))
    return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required
def userLogout(request):
    """Users get sent here temporarily when logging out."""

    logout(request)
    return HttpResponseRedirect('/')


@login_required
def editProfile(request):
    """
    Edit profile view.
    Basically a single form.
    """

    # if it's a POST, i.e. the user is submitting changes, time to enact them
    # i.e reconstruct his entire profile with the submitted data
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(request.POST, instance=profile)
        except:
            form = UserProfileForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                profile = form.save(commit=False)
                user = request.user
                profile.user = user
                profile.user.save()
                try:
                    profile.avatar = request.FILES['avatar']
                except:
                    pass
                profile.save()
        return HttpResponseRedirect(reverse('userProfile'))
    else:
        # otherwise pass a bunch of objects to our template and call it a day
        try:
            profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=profile)
        except:
            form = UserProfileForm()
    return render(request, 'stove/editProfile.html', {'user_profile_form': form, 'UserProfile': UserProfile.objects.get(user=request.user)})


def attendEvents(request):
    """
    Attend events view.
    Basically a formset that allows users to tick attendance. That's all there is to it, really.
    """

    context_dict = {}
    event_list = Event.objects.all().order_by('startDate')
    EventFormSet = formset_factory(EventCheckbox, extra=len(event_list))
    count = 0
    if request.method == 'POST':
        # have we been given a few events to attend? Good!
        formset = EventFormSet(request.POST)
        for form in formset:
            # if event X is checked, make sure we're attending. If not, make sure we're not attending.
            if form.is_valid() and form.cleaned_data == {}:
                EventAttendance.objects.filter(event=event_list[count], user=request.user).delete()
            else:
                EventAttendance.objects.get_or_create(event=event_list[count], user=request.user)
            count += 1
        return HttpResponseRedirect(reverse('userProfile'))
    formset = EventFormSet()
    eventsWithAttendance = []
    for event in event_list:
        # tick the relevant boxes in the formset to make sure the starting data is consistent
        checked = EventAttendance.objects.filter(event=event, user=request.user).exists()
        if checked:
            checked = "checked"
        else:
            checked = ""
        eventsWithAttendance += [{'event': event, 'checked': checked}]
    context_dict = {'eventswithattendance': eventsWithAttendance, 'formset': formset}
    return render(request, 'stove/attendEvents.html', context_dict)


def whatsOn(request):
    """
    What's on view.
    Renders a list of all events, which we pass down to the template.
    """

    context_dict = {}
    events = Event.objects.all().order_by('startDate')
    context_dict = {'events': events}
    return render(request, 'stove/whatsOn.html', context_dict)


def termsConditions(request):
    """
    Terms and conditions view.
    A glorified static page.
    """

    return render(request, 'stove/termsConditions.html')


@staff_member_required
def demographics(request):
    """
    Demographics view.
    Takes objects, calculates data and passes it down to the template for rendering
    All the nice rendering stuff is handled by D3 (with C3 as a wrapper) so we don't have to worry about things here
    """

    # all the gender information is extracted from db
    not_disclosed = UserProfile.objects.filter(gender=0).count()
    male = UserProfile.objects.filter(gender=1).count()
    female = UserProfile.objects.filter(gender=2).count()

    context_dict = {'title': "Demographics",
                    'male': male,
                    'female': female,
                    'not_disclosed': not_disclosed}

    # Extracting the number of user ticks for each preference category using an array of this type:
    # [pref0.subpref0, pref0.subpref1, ... pref0.subprefN, pref1.subpref0, .... pref1.subprefM, ...., prefP.subprefQ]
    # UserPreference.objects.filter(preference = sub_preferences_nonnumbered_list[count] - the number of ticks is
    # Category  = list of cats
    preferences = Preference.objects.all()
    prefCount = {}
    prefGendered = [{}, {}, {}]
    prefAged = [{}, {}, {}, {}, {}]
    genderPrefd = {}
    agePrefd = {}

    # This generates all statistics that have anything to do with preferences.
    # Anyone looking at this: tread with care, and do take reasonable anaesthetic precautions.
    for pref in preferences:
        subprefs = SubPreference.objects.filter(preference=pref)
        count = 0
        countGendered = [0, 0, 0]
        countAged = [0, 0, 0, 0, 0]
        for subpref in subprefs:
            userprefs = UserPreference.objects.filter(preference=subpref)
            count += len(userprefs)
            for up in userprefs:
                prof = UserProfile.objects.get(user=up.user)
                countGendered[prof.gender] += 1
                age = date.today().year - prof.dateOfBirth.year - ((date.today().month, date.today().day) < (prof.dateOfBirth.month, prof.dateOfBirth.day))
                if age < 18:
                    countAged[0] += 1
                elif age < 25:
                    countAged[1] += 1
                elif age < 40:
                    countAged[2] += 1
                elif age < 60:
                    countAged[3] += 1
                else:
                    countAged[4] += 1
        prefCount[pref.name.encode('ascii')] = count
        prefGendered[0][pref.name.encode('ascii')] = countGendered[0]
        prefGendered[1][pref.name.encode('ascii')] = countGendered[1]
        prefGendered[2][pref.name.encode('ascii')] = countGendered[2]
        prefAged[0][pref.name.encode('ascii')] = countAged[0]
        prefAged[1][pref.name.encode('ascii')] = countAged[1]
        prefAged[2][pref.name.encode('ascii')] = countAged[2]
        prefAged[3][pref.name.encode('ascii')] = countAged[3]
        prefAged[4][pref.name.encode('ascii')] = countAged[4]
        genderPrefd[pref.name.encode('ascii')] = countGendered + []
        agePrefd[pref.name.encode('ascii')] = countAged + []

    context_dict['prefdict'] = prefCount
    context_dict['prefgendered'] = prefGendered
    context_dict['prefaged'] = prefAged
    context_dict['genderprefd'] = genderPrefd
    context_dict['ageprefd'] = agePrefd

    # extract ages for the sake of making a chart thingy. 5 categories because pie charts don't work with big sets of disparate values
    ageCount = {"Under18": 0, "1824": 0, "2539": 0, "4059": 0, "Over60": 0}
    ageGendered = [[], [], []]
    ageGendered[0] = {"Under18": 0, "1824": 0, "2539": 0, "4059": 0, "Over60": 0}
    ageGendered[1] = {"Under18": 0, "1824": 0, "2539": 0, "4059": 0, "Over60": 0}
    ageGendered[2] = {"Under18": 0, "1824": 0, "2539": 0, "4059": 0, "Over60": 0}
    genderAged = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for prof in UserProfile.objects.all():
        age = date.today().year - prof.dateOfBirth.year - ((date.today().month, date.today().day) < (prof.dateOfBirth.month, prof.dateOfBirth.day))
        if age < 18:
            ageCount["Under18"] += 1
            ageGendered[prof.gender]["Under18"] += 1
            genderAged[0][prof.gender] += 1
        elif age < 25:
            ageCount["1824"] += 1
            ageGendered[prof.gender]["1824"] += 1
            genderAged[1][prof.gender] += 1
        elif age < 40:
            ageCount["2539"] += 1
            ageGendered[prof.gender]["2539"] += 1
            genderAged[2][prof.gender] += 1
        elif age < 60:
            ageCount["4059"] += 1
            ageGendered[prof.gender]["4059"] += 1
            genderAged[3][prof.gender] += 1
        else:
            ageCount["Over60"] += 1
            ageGendered[prof.gender]["Over60"] += 1
            genderAged[4][prof.gender] += 1

    count = len(UserPreference.objects.filter(preference=subpref))
    context_dict['agedict'] = ageCount
    context_dict['agegendered'] = ageGendered
    context_dict['genderaged'] = genderAged

    return render(request, 'admin/stove/demographics.html', context_dict)

# Statistical methods:


def median(seq):
    """
    Finds out the median from a list.
    :param seq: List to process.
    """

    return sorted(seq)[len(seq) / 2]


def uniq(seq):
    """
    Copies a list, but without duplicates.
    :param seq: List to process.
    """

    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


@staff_member_required
def profiler(request):
    """
    Event profiler page.
    Takes an event, collects everybody who attends it and makes semi-meaningful statistics.
    """

    context_dict = {'title': "Event profiler"}
    if request.method == 'POST':
        # have we been given an event to profile? Good!
        form = EventDropdown(request.POST)
        if form.is_valid():
            event = form.cleaned_data['events']
            # get attendance data
            attendance = EventAttendance.objects.filter(event=event)
            numAttendees = len(attendance)
            # if no one's going we shouldn't bother
            if numAttendees < 1:
                context_dict['err'] = "Can't build statistics: no one is attending " + event.name + "!"
            else:
                context_dict['eventname'] = event.name
                context_dict['numattendees'] = numAttendees
                ages = []
                genders = []
                postcodes = []
                cats = []
                otherevents = []
                # for every attendee, add the relevant data to our pool
                for i in attendance:
                    user = UserProfile.objects.get(user=i.user)
                    ages += [date.today().year - user.dateOfBirth.year - ((date.today().month, date.today().day) < (user.dateOfBirth.month, user.dateOfBirth.day))]
                    genders += [user.gender]
                    postcodes += [user.postcode.replace(' ', '')[:-3]]
                    for j in UserPreference.objects.filter(user=i.user):
                        cats += [j.preference.name]
                    for j in EventAttendance.objects.filter(user=i.user).exclude(event=event):
                        otherevents += [j.event]
                # and pass that data on for rendering
                context_dict['age'] = sum(ages) / len(ages)
                context_dict['gender'] = median(genders)
                context_dict['postcode'] = median(postcodes)
                context_dict['cats'] = uniq(cats)
                context_dict['otherevents'] = otherevents
        else:
            context_dict['err'] = "You haven't chosen an event!"
    context_dict['form'] = EventDropdown()
    return render(request, 'admin/stove/profiler.html', context_dict)
