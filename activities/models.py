from django.db import models

class hashtags(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=30,verbose_name="name")
    pic = models.ImageField(upload_to = 'uploads/hashtags/',verbose_name="pic",blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class places(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=30,verbose_name="place")
    pic = models.ImageField(upload_to = 'uploads/places/',verbose_name="pic",blank=True, null=True)
    
    def __str__(self):
        return self.name

class communities(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=30,verbose_name="place")
    pic = models.ImageField(upload_to = 'uploads/places/',verbose_name="pic",blank=True, null=True)
    
    def __str__(self):
        return self.name


class activities(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50,verbose_name="title")
    description = models.CharField(max_length=1000,verbose_name="description")

    hashtag = models.ForeignKey("activities.hashtags",on_delete = models.CASCADE, verbose_name='hashtags')
    place = models.ForeignKey("activities.places",on_delete = models.CASCADE, verbose_name='area')
    community = models.ForeignKey("activities.communities",on_delete = models.CASCADE, verbose_name='community')

    m_time = models.DateTimeField(auto_now_add=False)
    creator = models.ForeignKey("account.usercore",on_delete = models.CASCADE, verbose_name='creator')
    activity = models.CharField(max_length=50,verbose_name="link")

    def __str__(self):
        return self.name