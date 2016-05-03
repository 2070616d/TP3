#!/usr/local/bin python2.7
# -*- coding: iso-8859-1 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tp3_project.settings')

import django
django.setup()

from stove import *
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

def populate():
    me = Site.objects.get(pk=1)
    me.name = "MyStove"
    me.domain = "mystove.pythonanywhere.com"
    me.save()
    test1 = add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25')
    doctor = add_user('TheDoctor', 'The', 'Doctor', 'G3 6JR', 'TARDIS', 'hateDaleks@gmail.com', '1934-08-13')

    add_admin('adm', 'mystovenetwork@gmail.com', 'password')

    craftivism = add_event_category('Craftivism')
    brave = add_event_category('Brave New Words')
    wayfinding = add_event_category('Cultural Wayfinding')
    designcommission = add_event_category('Building Design Commission')
    agm = add_event_category('AGM')
    lgbtfilm = add_event_category('LGBT Film Screening')
    submerge = add_event_category('Submerge')
    qofscale = add_event_category('A Question of Scale')
    reel2reel = add_event_category('Reel to Real Film Screening')
    communityevent = add_event_category('Community Event')
    inbetween = add_event_category('InBetween')
    musicconf = add_event_category('Music Conference')
    architecture = add_event_category('Architecture')
    showcase = add_event_category('showcase')

    reel2realfilm4 = add_event(reel2reel, 'Reel to Real Film Screening 4', '2016-02-23 09:00', '2016-02-23 17:00', '2', '')
    inbetweenRes = add_event(inbetween, 'Inbetween Residency', '2016-03-01 09:00', '2016-07-30 17:00', '2', '')

    culturalWayfindingNorway = add_event(wayfinding, 'Cultural Wayfinding - Norway Event', '2016-03-01 09:00', '2016-03-01 17:00', '1', '')

    dumfriesMusicCon = add_event(musicconf, 'Dumfries Music Conference', '2016-03-01 09:00', '2016-03-01 17:00', 'All', 'http://www.thestove.org/dmc')

    festivalArchitecture = add_event(architecture, '2016 Festival of Architecture', '2016-03-08 09:00', '2016-03-08 17:00', '1', '')

    reel2realfilm5 = add_event(reel2reel, 'Reel to Real Film Screening 5', '2016-03-22 09:00', '2016-03-22 17:00', '1 and 2', '')

    reel2realfilm6 = add_event(reel2reel, 'Reel to Real Film Screening 6', '2016-04-19 09:00', '2016-04-19 17:00', '1 and 2', '')

    guidNychburris = add_event(communityevent, 'Guid Nychburris', '2016-06-18 09:00', '2016-06-18 17:00', '1 and 2', '')

    nithraid = add_event(communityevent, 'Nithraid', '2016-08-20 09:00', '2016-08-20 17:00', '1 and 2', 'http://www.thestove.org/nithraid')

    smallTownSounds = add_event(communityevent, 'Small Town Sounds', '2016-12-01 09:00', '2016-12-01 17:00', '1 and 2', 'http://smalltownsounds.co.uk/about/')

    add_event_attendance(reel2realfilm4, doctor)

    craft = add_preference('Craft')
    food = add_preference('Food')
    lensBased = add_preference('Lens-based')
    music = add_preference('Music')
    performance = add_preference('Performance')
    publicArt = add_preference('Public art')
    visualArt = add_preference('Visual art')
    word = add_preference('Word')

    craftivism = add_sub_preference(craft, 'Craftivism')
    workshops_craft = add_sub_preference(craft, 'Workshops')
    exhibitions_craft = add_sub_preference(craft, 'Exhibitions')

    workshops_food = add_sub_preference(food, 'Workshops')
    outreach = add_sub_preference(food, 'Outreach')

    film_screenings = add_sub_preference(lensBased, 'Film screenings')
    photography = add_sub_preference(lensBased, 'Photography')

    acoustic_gigs = add_sub_preference(music, 'Acoustic gigs')
    open_mic = add_sub_preference(music, 'Open mic')
	
    theatre = add_sub_preference(performance, 'Theatre')
    dance = add_sub_preference(performance, 'Dance')

    debate = add_sub_preference(publicArt, 'Debate')
    outdoor_events = add_sub_preference(publicArt, 'Outdoor events')

    exhibitions_visual_art = add_sub_preference(visualArt, 'Exhibitions')
    commissions = add_sub_preference(visualArt, 'Commissions')
	
    spoken_word = add_sub_preference(word, 'Spoken word')
    workshops_word = add_sub_preference(word, 'Workshops')
    readings = add_sub_preference(word, 'Readings')

    add_user_pref(craftivism, doctor)
    add_user_pref(exhibitions_craft, doctor)
    add_user_pref(photography, doctor)
    add_user_pref(acoustic_gigs, test1)
    add_user_pref(open_mic, test1)
    add_user_pref(theatre, test1)

    soups = add_cafe_cat("Today's Soups (with bread)")
    quiche = add_cafe_cat('Quiche')
    sandwiches = add_cafe_cat("Today's Sandwiches")
    smoothies = add_cafe_cat('Healthy Hit Smoothies')
    coffee = add_cafe_cat('Fairtrade, Rainforest Alliance & UTZ Certified Coffee')
    teas = add_cafe_cat('Ethically Sourced Loose Leaf Teas')

    add_cafe_item('Tomato', 2.00, soups)
    add_cafe_item('Lentil', 2.00, soups)
    add_cafe_item("Ham 'n' Cheese", 3.60, quiche)
    add_cafe_item('Tomato', 3.30, quiche)
    add_cafe_item('Rainbow', 4.00, quiche)
    add_cafe_item('Latte', 1.80, coffee)
    add_cafe_item('Cappuccino', 2.50, coffee)
    add_cafe_item('Flat white', 2.00, coffee)
    add_cafe_item('Americano', 2.00, coffee)
    add_cafe_item('Espresso', 1.80, coffee)
    add_cafe_item('Hot chocolate', 1.50, coffee)
    add_cafe_item('Cream and marshmallows', 2.10, coffee)
    add_cafe_item('Chai latte', 2.00, coffee)
    add_cafe_item('Dirty Chai', 2.00, coffee)
    add_cafe_item('Scottish Breakfast', 1.20, teas)
    add_cafe_item('Decaff', 1.50, teas)
    add_cafe_item('Earl Grey', 1.50, teas)
    add_cafe_item('Sencha Green', 1.70, teas)
    add_cafe_item('Peppermint', 1.75, teas)
    add_cafe_item('Camomile', 1.80, teas)
    add_cafe_item('Zesty lemon rooibos', 2.00, teas)
    add_cafe_item('Red berry', 2.00, teas)

def add_user(userName, firstName, lastName, postcode, password, email, dateOfBirth):
    user = User.objects.create_user(userName, email, password)
    user.first_name=firstName
    user.last_name=lastName
    user.save()
    userProfile = stove.models.UserProfile.objects.get_or_create(user=user, postcode=postcode, dateOfBirth=dateOfBirth)[0]
    return user


def add_event_category(categoryName):
    catName = stove.models.EventCategory.objects.get_or_create(name=categoryName)[0]
    return catName


def add_event(category, name, startDate, endDate, location, info):
    event = stove.models.Event.objects.get_or_create(category=category,
                                                     name=name,
                                                     startDate=startDate,
                                                     endDate=endDate,
                                                     location=location,
                                                     info=info)[0]
                                                     #numberOfAttendees=numberOfAttendees)[0]
    return event


def add_event_attendance(Event, UserAttending):
    event_attendance = stove.models.EventAttendance.objects.get_or_create(event=Event,
                                                                          user=UserAttending)[0]
    return event_attendance


def add_preference(preferenceName):
    preference = stove.models.Preference.objects.get_or_create(name=preferenceName)[0]
    return preference


def add_sub_preference(preference, SubPreferenceName):
    sub_preference = stove.models.SubPreference.objects.get_or_create(preference=preference,
                                                                       name=SubPreferenceName)[0]
    return sub_preference


def add_user_pref(preference, user):
    user_preference = stove.models.UserPreference.objects.get_or_create(preference=preference,
                                                                        user=user)[0]
    return user_preference


def add_admin(adminName, adminEmail, adminPassword):
    admin = User.objects.create_superuser(adminName, adminEmail, adminPassword)
    admin.first_name="Web"
    admin.last_name="Master"
    admin.save()
    userProfile = stove.models.UserProfile.objects.get_or_create(user=admin, postcode="DG1 2BJ", dateOfBirth='2016-01-01')[0]
    return admin


def add_cafe_cat(catName):
    cat = stove.models.CafeCategory.objects.get_or_create(name=catName)[0]
    return cat


def add_cafe_item(itemName, price, cat):
    item = stove.models.CafeItem.objects.get_or_create(name=itemName, price=price, category=cat)[0]
    return item


if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tp3_project.settings')
    import stove.models

    populate()
