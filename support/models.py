from django.db import models
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Service(models.Model):
    subject = models.CharField(max_length=200)
    icon = models.CharField(max_length=200, default='bi bi-briefcase')
    message = models.TextField()
    photo = ResizedImageField(size=[1024, 768], crop=['middle', 'center'], upload_to='services/photo', default='services/photo/services.jpg')
    slug = models.SlugField(max_length=250, null=True, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)
        super().save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def get_absolute_url(self):
        from django.shortcuts import reverse
        return reverse('service', kwargs={'id': self.pk, 'slug': self.slug})