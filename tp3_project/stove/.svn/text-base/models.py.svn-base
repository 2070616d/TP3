# -*- coding: iso-8859-1 -*-
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from image_cropping import ImageRatioField


class UserProfile(models.Model):
    """
    User profile model.
    Contains all the data that the default django user model cannot store, and is built on top of that.
    """

    user = models.OneToOneField(User)
    postcode = models.CharField(max_length=8, unique=False)
    dateOfBirth = models.DateField()
    CATEGORY_CHOICES = (
        (0, 'Other gender or prefer not to disclose'),
        (1, 'Male'),
        (2, 'Female'),
    )
    gender = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
    avatar = models.ImageField('profile picture', upload_to='avatars', blank=True)
    avatarCropping = ImageRatioField('avatar', '200x200')

    def __unicode__(self):
        return self.user.username


@receiver(post_delete, sender=UserProfile)
def delete(sender, instance=None, **kwargs):
    """
    Upon deleting a user profile, delete its corresponding account.
    :param sender: Required from binding to signal, ignore me.
    :param instance: The profile being deleted.
    :param kwargs: Required from binding to signal, ignore me.
    """

    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()


class Preference(models.Model):
    """
    Preference model.
    Contains only a name string. Sub-preferences bind to this.
    """

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class SubPreference(models.Model):
    """
    Sub-preference model.
    Contains a name and binds to a corresponding preference.
    Connects to users via user preferences.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    UserPreference = models.ManyToManyField(User, through='UserPreference')

    def __unicode__(self):
        return self.name


class UserPreference(models.Model):
    """
    User preference model.
    Hooks up users and sub-preferences together.
    """

    preference = models.ForeignKey(SubPreference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class EventCategory(models.Model):
    """
    Event category model.
    Contains only a name string. Events bind to this.
    """

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Event categories"


class Event(models.Model):
    """
    Event model.
    Contains a whole host of relevant information, such as name, type, description, picture, data, etc..
    Connects to users via event attendance.
    """

    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    startDate = models.DateTimeField(blank=True)
    endDate = models.DateTimeField(blank=True)
    location = models.CharField(max_length=128)
    info = models.CharField(max_length=1024)
    caterTo = models.ForeignKey(SubPreference, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField('picture', upload_to='event_pictures', blank=True)
    pictureCropping = ImageRatioField('picture', '333x222')
    Attendance = models.ManyToManyField(User, through='EventAttendance')

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=Event)
def sendNotifications(sender, instance, **kwargs):
    """
    Send email notifications to users who might be interested in a newly-added event.
    :param sender: Required from binding to signal, ignore me.
    :param instance: The event being added.
    :param kwargs: Required from binding to signal, ignore me.
    """

    for pref in UserPreference.objects.filter(preference=instance.caterTo):
        send_mail('New events you might be interested in on MyStove',
                  'Hey! We thought you might be interested in \'' +
                  instance.name + '\', based on your stated preferences. Go on MyStove to see more!',
                  None, [pref.user.email], fail_silently=True)


class EventAttendance(models.Model):
    """
    Event attendance model.
    Hooks up users and events together.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User)


class CafeCategory(models.Model):
    """
    Cafe category model.
    Contains only a name string. Cafe items bind to this.
    """

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cafe categories"


class CafeItem(models.Model):
    """
    Cafe item model.
    Contains a name, a price and binds to a corresponding category.
    """

    category = models.ForeignKey(CafeCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    price = models.FloatField(default=0)
    Likes = models.ManyToManyField(User, through='CafeItemLike')

    def __unicode__(self):
        return self.name


class CafeItemLike(models.Model):
    """
    Cafe like model.
    Hooks up users and cafe items together.
    """

    item = models.ForeignKey(CafeItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
