# -*- coding: iso-8859-1 -*-
from django.test import TestCase
from django.core import urlresolvers
from django.contrib.auth.models import User
from datetime import date
import stove
from stove import *


def add_user(userName, firstName, lastName,
             postcode, password, email, dateOfBirth, gender):
    user = User.objects.create_user(userName, email, password)
    user.first_name = firstName
    user.last_name = lastName
    user.save()
    userProfile = stove.models.UserProfile.objects.get_or_create(user=user, postcode=postcode, dateOfBirth=dateOfBirth, gender=gender)[0]
    return (user, userProfile)


def add_event_category(name):
    name = stove.models.EventCategory.objects.get_or_create(name=name)[0]
    return name


def add_event(category, name, startDate, endDate, location, info):
    event = stove.models.Event.objects.get_or_create(category=category,
                                                     name=name,
                                                     startDate=startDate,
                                                     endDate=endDate,
                                                     location=location,
                                                     info=info)[0]
    return event


def add_event_attendance(Event, UserAttending):
    event_attendance = stove.models.EventAttendance.objects.get_or_create(event=Event,
                                                                          user=UserAttending)[0]
    return event_attendance


def add_preference(name):
    preference = stove.models.Preference.objects.get_or_create(name=name)[0]
    return preference


def add_sub_preference(preference, name):
    sub_preference = stove.models.SubPreference.objects.get_or_create(preference=preference,
                                                                      name=name)[0]
    return sub_preference


def add_user_pref(preference, user):
    user_preference = stove.models.UserPreference.objects.get_or_create(preference=preference,
                                                                        user=user)[0]
    return user_preference


def add_admin(adminName, adminEmail, adminPassword):
    admin = User.objects.create_superuser(adminName, adminEmail, adminPassword)
    admin.first_name = "Web"
    admin.last_name = "Master"
    admin.save()
    stove.models.UserProfile.objects.get_or_create(user=admin, postcode="DG1 2BJ", dateOfBirth='2016-01-01')
    return admin


def add_cafe_cat(name):
    cat = stove.models.CafeCategory.objects.get_or_create(name=name)[0]
    return cat


def add_cafe_item(name, price, cat):
    item = stove.models.CafeItem.objects.get_or_create(name=name, price=price, category=cat)[0]
    return item


def add_cafe_like(item, user):
    like = stove.models.CafeItemLike.objects.get_or_create(item=item, user=user)[0]
    return like


class ModelTests(TestCase):
    def test_user(self):
        user = add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        self.assertEqual(user[0].username, 'test1')
        self.assertEqual(user[1].postcode, 'G2 3HU')
        self.assertEqual(user[1].dateOfBirth, '1983-11-25')
        self.assertEqual(user[1].gender, '1')
        self.assertEqual(str(user[1]), user[0].username)
        self.assertNotEqual(user[0].username, 'tes21')
        self.assertNotEqual(user[1].postcode, 'G3 3HU')
        self.assertNotEqual(user[1].dateOfBirth, '1981-11-25')
        self.assertNotEqual(user[1].gender, '2')
        user[1].delete()
        shouldbetrue = False
        try:
            User.objects.get(username='test1')
        except:
            shouldbetrue = True
        self.assertTrue(shouldbetrue)

    def test_event(self):
        craftivism = add_event_category('Craftivism')
        artcop1 = add_event(craftivism, 'ArtCOP Slow-activism',
                            '2015-10-28 09:00', '2015-11-25 17:00', '1',
                            'http://www.thestove.org/event/craftivism-stitch-in-at-the-stove')
        self.assertEqual(craftivism.name, 'Craftivism')
        self.assertEqual(artcop1.category, craftivism)
        self.assertEqual(artcop1.name, 'ArtCOP Slow-activism')
        self.assertEqual(artcop1.startDate, '2015-10-28 09:00')
        self.assertEqual(artcop1.endDate, '2015-11-25 17:00')
        self.assertEqual(artcop1.location, '1')
        self.assertEqual(artcop1.info, 'http://www.thestove.org/event/craftivism-stitch-in-at-the-stove')
        self.assertNotEqual(craftivism.name, 'Croftivismus')
        self.assertNotEqual(artcop1.name, 'ArtCooP Slow-activism')
        self.assertNotEqual(artcop1.startDate, '2012-10-28 09:00')
        self.assertNotEqual(artcop1.endDate, '2012-11-25 17:00')
        self.assertNotEqual(artcop1.location, '22')
        self.assertNotEqual(artcop1.info, 'http://www.thestave.org/event/craftivism-stitch-in-at-the-stove')

    def test_cafe(self):
        drinks = add_cafe_cat('drinks')
        self.assertEqual(drinks.name, 'drinks')
        self.assertNotEqual(drinks.name, 'stinks')
        bites = add_cafe_cat('bites')
        self.assertEqual(bites.name, 'bites')
        self.assertNotEqual(bites.name, 'mites')
        sweets = add_cafe_cat('sweets')
        self.assertEqual(sweets.name, 'sweets')
        self.assertNotEqual(sweets.name, 'meats')
        juice = add_cafe_cat('soft drinks')
        self.assertEqual(juice.name, 'soft drinks')
        self.assertNotEqual(juice.name, 'bucky')
        self.assertEqual(str(juice), juice.name)

        latte = add_cafe_item('latte', 2.30, drinks)
        self.assertEqual(latte.category, drinks)
        self.assertEqual(latte.price, 2.30)
        self.assertEqual(latte.name, 'latte')
        toastie = add_cafe_item('cheese toastie', 1.30, bites)
        self.assertEqual(toastie.category, bites)
        self.assertEqual(toastie.price, 1.30)
        self.assertEqual(toastie.name, 'cheese toastie')
        mousse = add_cafe_item('chocolate mousse', 3.30, sweets)
        self.assertEqual(mousse.category, sweets)
        self.assertEqual(mousse.price, 3.30)
        self.assertEqual(mousse.name, 'chocolate mousse')
        oj = add_cafe_item('orange juice', 2.00, juice)
        self.assertEqual(oj.category, juice)
        self.assertEqual(oj.price, 2.00)
        self.assertEqual(oj.name, 'orange juice')
        murica = add_cafe_item('americano', 1.80, drinks)
        self.assertEqual(murica.category, drinks)
        self.assertEqual(murica.price, 1.80)
        self.assertEqual(murica.name, 'americano')
        self.assertEqual(str(murica), murica.name)

    def test_preference(self):
        music = add_preference('music')
        self.assertEqual(music.name, 'music')
        self.assertNotEqual(music.name, 'film')
        theatre = add_preference('theatre')
        self.assertEqual(theatre.name, 'theatre')
        self.assertNotEqual(theatre.name, 'drama')
        self.assertEqual(str(theatre), theatre.name)

        gig = add_sub_preference(music, 'gig')
        self.assertEqual(gig.preference, music)
        self.assertEqual(gig.name, 'gig')
        concert = add_sub_preference(music, 'concert')
        self.assertEqual(concert.preference, music)
        self.assertEqual(concert.name, 'concert')
        shakespeare = add_sub_preference(theatre, 'shakespeare')
        self.assertEqual(shakespeare.preference, theatre)
        self.assertEqual(shakespeare.name, 'shakespeare')
        self.assertEqual(str(shakespeare), shakespeare.name)


class ViewTests(TestCase):
    def test_invalid_page(self):
        response = self.client.get('/pagethatdoesntexit/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/admin/pagethatdoesntexit/')
        self.assertEqual(response.status_code, 404)

    def test_valid_page(self):
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 404)
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 404)

    def test_login(self):
        user = add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        response = self.client.post('/login/', {'username': 'test1'})
        self.assertContains(response, 'password')
        response = self.client.post('/login/', {'username': 'test1', 'password': 'WRONG'})
        self.assertContains(response, 'password')
        response = self.client.post('/login/', {'username': 'test1', 'password': 'asdf'})
        self.assertEqual(int(self.client.session['_auth_user_id']), user[0].pk)

    def test_csv(self):
        add_admin("lala", "lala@lala.com", "lala")
        self.client.login(username="lala", password="lala")
        change_url = urlresolvers.reverse('admin:stove_userprofile_changelist')
        data = {'action': 'download_csv', '_selected_action': User.objects.all().values_list('pk', flat=True)}
        response = self.client.post(change_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Web,Master" in str(response))

    def test_cafe(self):
        drinks = add_cafe_cat('drinks')
        item = add_cafe_item('latte', 2.30, drinks)
        response = self.client.get('/cafe/')
        self.assertContains(response, 'latte')
        self.assertContains(response, 'drinks')
        self.assertContains(response, '0 like')
        user = add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        add_cafe_like(user=user[0], item=item)
        response = self.client.get('/cafe/')
        self.assertContains(response, '1 like')
        self.client.login(username="test1", password="asdf")
        response = self.client.post('/cafeItemLike/', {'pk': item.pk})
        self.assertEqual(response.status_code, 200)
        shouldbetrue = False
        try:
            stove.models.CafeItemLike.objects.get(user=user[0], item=item)
        except:
            shouldbetrue = True
        self.assertTrue(shouldbetrue)
        response = self.client.post('/cafeItemLike/', {'pk': item.pk})
        self.assertEqual(response.status_code, 200)
        stove.models.CafeItemLike.objects.get(user=user[0], item=item)

    def test_index(self):
        response = self.client.get('/')
        self.assertContains(response, 'Welcome')
        add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        self.client.login(username="test1", password="asdf")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        response = self.client.get('/')
        user_form = response.context['user_form']
        profile_form = response.context['profile_form']
        user_data = user_form.initial
        profile_data = profile_form.initial
        user_data['username'] = 'jswiftyo'
        user_data['email'] = 'jswiftyo@thatan.com'
        user_data['password'] = 'lelelelele'
        user_data['password2'] = 'lelelelele'
        user_data['tandc'] = True
        profile_data['first_name'] = 'Jonathan'
        profile_data['last_name'] = 'Swift'
        profile_data['postcode'] = 'EN8 9SL'
        profile_data['dateOfBirth'] = '06/06/2006'
        profile_data['gender'] = 1
        user_data.update(profile_data)
        response = self.client.post('/registration/', user_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/userProfile/')
        self.assertContains(response, 'Jonathan')
        self.assertContains(response, 'Swift')
        self.assertContains(response, 'EN8 9SL')
        self.assertContains(response, '6 Jun 2006')

        response = self.client.get('/registrationSocial/')
        response = self.client.get('/socialLoginFinalise/')

    def test_userprofile(self):
        add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        self.client.login(username="test1", password="asdf")
        response = self.client.get('/userProfile/')
        self.assertContains(response, 'John')
        self.assertContains(response, 'Smith')
        self.assertContains(response, 'G2 3HU')
        self.assertContains(response, '25 Nov 1983')
        response = self.client.get('/editProfile/')
        self.assertContains(response, 'G2 3HU')
        self.assertContains(response, '25/11/1983')
        form = response.context['user_profile_form']
        data = form.initial
        data['postcode'] = 'EN8 9SL'
        data['dateOfBirth'] = '06/06/2006'
        data['avatar'] = ''
        response = self.client.post('/editProfile/', data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/userProfile/')
        self.assertContains(response, 'EN8 9SL')
        self.assertContains(response, '6 Jun 2006')

    def test_preferences(self):
        user = add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        music = add_preference('music')
        gig = add_sub_preference(music, 'gig')
        concert = add_sub_preference(music, 'concert')
        not_concert = add_sub_preference(music, 'not concert')

        self.client.login(username="test1", password="asdf")
        response = self.client.get('/userProfile/')
        self.assertContains(response, 'music')
        self.assertContains(response, 'gig')
        self.assertContains(response, 'concert')
        add_user_pref(gig, user[0])
        response = self.client.get('/preferences/')
        stove.models.UserPreference.objects.get(preference=gig)
        formset_data = response.context['formset'].management_form.initial
        data = dict([
            ('%s-%s' % (response.context['formset'].prefix, key), value if value is not None else '')
            for key, value
            in formset_data.iteritems()
        ])
        data['form-1-checked'] = True
        response = self.client.post('/preferences/', data)
        stove.models.UserPreference.objects.get(preference=concert)
        shouldbetrue = False
        try:
            stove.models.UserPreference.objects.get(preference=not_concert)
        except:
            shouldbetrue = True
        self.assertTrue(shouldbetrue)

    def test_events(self):
        test1 = add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        craftivism = add_event_category('Craftivism')
        artcop1 = add_event(craftivism, 'ArtCOP Slow-activism', '2015-10-28 09:00', '2015-11-25 17:00', '1', 'http://www.thestove.org/event/craftivism-stitch-in-at-the-stove')

        response = self.client.get('/whatsOn/')
        self.assertContains(response, 'ArtCOP Slow-activism')
        self.assertContains(response, '28 Oct 2015')
        self.assertContains(response, '9 a.m.')
        self.assertContains(response, '25 Nov 2015')
        self.assertContains(response, '5 p.m.')
        self.assertContains(response, 'location: 1')
        self.assertContains(response, 'For more information: http://www.thestove.org/event/craftivism-stitch-in-at-the-stove')

        self.client.login(username="test1", password="asdf")
        response = self.client.get('/attendEvents/')
        self.assertContains(response, 'Craftivism')
        self.assertContains(response, 'ArtCOP Slow-activism')
        self.assertContains(response, '28 Oct 2015, 9 a.m.')
        self.assertContains(response, '25 Nov 2015, 5 p.m.')
        self.assertContains(response, '1')
        self.assertContains(response, 'http://www.thestove.org/event/craftivism-stitch-in-at-the-stove')
        add_event_attendance(artcop1, test1[0])

        response = self.client.get('/userProfile/')
        self.assertContains(response, 'ArtCOP Slow-activism')
        self.assertContains(response, '28 Oct 2015, 9 a.m.')
        self.assertContains(response, '25 Nov 2015, 5 p.m.')

        response = self.client.get('/attendEvents/')
        stove.models.EventAttendance.objects.get(event=artcop1)
        formset_data = response.context['formset'].management_form.initial
        data = dict([
            ('%s-%s' % (response.context['formset'].prefix, key), value if value is not None else '')
            for key, value
            in formset_data.iteritems()
        ])
        data['form-0-checked'] = True
        response = self.client.post('/attendEvents/', data)
        stove.models.EventAttendance.objects.get(event=artcop1)

    def test_logout(self):
        add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        self.client.login(username="test1", password="asdf")
        self.client.get('/logout/')
        try:
            int(self.client.session['_auth_user_id'])
        except:
            return
        raise

    def test_tAndc(self):
        response = self.client.get('/termsConditions/')
        self.assertContains(response, 'Terms & Conditions')

    def test_demographics(self):
        add_admin('admin1', 'admin@gmail.com', 'adOne')
        user1 = add_user('test1', 'John', 'Smith', 'G2 3HU', 'asdf', 'asdf@gmail.com', '1983-11-25', '1')
        user2 = add_user('test2', 'June', 'Smith', 'G2 3HU', 'asdg', 'asdg@gmail.com', '1985-11-25', '2')
        user3 = add_user('test3', 'January', 'Smith', 'G2 3HU', 'asdg', 'asdg@gmail.com', '1975-11-25', '2')
        user4 = add_user('test4', 'Jonno', 'Smith', 'G2 3HU', 'asdg', 'asdg@gmail.com', '1995-11-25', '2')
        user5 = add_user('test5', 'Jacques', 'Smith', 'G2 3HU', 'asdg', 'asdg@gmail.com', '1965-11-25', '2')
        user6 = add_user('test6', 'Jafar', 'Smith', 'G2 3HU', 'asdg', 'asdg@gmail.com', '1955-11-25', '2')
        user7 = add_user('test7', 'Jared', 'Smith', 'G2 3HU', 'asdg', 'asdg@gmail.com', '1945-11-25', '2')
        craftivism = add_event_category('Craftivism')
        artcop1 = add_event(craftivism, 'ArtCOP Slow-activism', '2015-10-28 09:00', '2015-11-25 17:00', '1', 'http://www.thestove.org/event/craftivism-stitch-in-at-the-stove')
        add_event(craftivism, 'ArtCOP Slow-activism 2', '2016-1-3 09:00', '2016-2-1 17:00', '1', 'http://www.thestove.org/event/craftivism-stitch-in-at-the-stove')
        artcop3 = add_event(craftivism, 'ArtCOP Slow-activism 718239649', '2016-1-3 09:00', '2016-2-1 17:00', '1', 'http://www.loser.com')
        music = add_preference('music')
        theatre = add_preference('theatre')
        gig = add_sub_preference(music, 'gig')
        concert = add_sub_preference(music, 'concert')
        shakespeare = add_sub_preference(theatre, 'shakespeare')
        add_user_pref(gig, user1[0])
        add_user_pref(concert, user1[0])
        add_user_pref(shakespeare, user2[0])
        add_event_attendance(artcop1, user2[0])
        add_event_attendance(artcop3, user1[0])
        add_event_attendance(artcop3, user2[0])
        add_event_attendance(artcop3, user3[0])
        add_event_attendance(artcop3, user4[0])
        add_event_attendance(artcop3, user5[0])
        add_event_attendance(artcop3, user6[0])
        add_event_attendance(artcop3, user7[0])
        self.client.login(username="admin1", password="adOne")
        response = self.client.get('/admin/demographics/')
        self.assertContains(response, 'Users by gender')
        self.assertContains(response, 'Users by categories of interest')
        self.assertContains(response, 'Users by age group')
        self.assertContains(response, 'Male')
        self.assertContains(response, 'Female')
        self.assertContains(response, 'music')
        self.assertContains(response, 'theatre')

        response = self.client.post('/admin/profiler/', {})
        self.assertContains(response, 'an event')

        response = self.client.post('/admin/profiler/', {'events': '1'})
        self.assertContains(response, (date.today().year - 1985 - ((date.today().month, date.today().day) < (11, 25))))
        self.assertContains(response, 'female')
        self.assertContains(response, 'shakespeare')
        self.assertContains(response, 'ArtCOP Slow-activism 2')

        response = self.client.post('/admin/profiler/', {'events': '2'})
        self.assertContains(response, 'no one')

        response = self.client.post('/admin/profiler/', {'events': '3'})
        self.assertEqual(response.status_code, 200)
