from django.db import models
from seeseehome import msg, testdata
from django.core.exceptions import ValidationError
from users.models import User
from django.core.validators import URLValidator

class LinkPostManager(models.Manager):
    ##### CREATE
    def _create_linkpost(self, description, url, writer):
        self.validate_description(description)
        if not self.is_valid_writeperm_to_linkpost(writer):
            raise ValidationError(msg.linkboard_linkpost_invalid_writer_perm)
        urlvalidator = URLValidator()
        urlvalidator(url)

        linkpost= self.model(description=description, url=url,
                writer=writer)

        linkpost.save(using=self._db)

        return linkpost

    def create_linkpost(self, description, url, writer):
        return self._create_linkpost(description=description, 
                url = url, writer=writer)
    
    def validate_description(self, description):
        if not description:
            raise ValueError(msg.boards_linkpost_description_must_be_set)
        elif len(description) > 255:
            raise ValidationError(msg.boards_linkpost_description_at_most_255)

    def is_valid_writeperm_to_linkpost(self, writer):
#       linkpost is allowed who has the permission higher than 'user'
        return bool(writer.userperm >= testdata.perm_member)

    def is_valid_readperm_to_linkpost(self, reader):
#       linkboard is allowed who has the permission equal or higher than 'user'
        return bool(reader.userperm >= testdata.perm_user)



class LinkPost(models.Model):
    objects = LinkPostManager()
    writer = models.ForeignKey(User)
    description = models.CharField(
                  help_text = "A description about the link",
                  max_length = 255,
              )

    url = models.URLField(
            help_text = "An URL for link to some information",
#           max_length = 200, # default : 200            
          )


#   It is used to show date posted in admin page 
    date_posted = models.DateTimeField(db_index=True, auto_now_add=True, 
            help_text = "It is used to show date when the link posted")
    
#   for showing description instead of object itself
    def __unicode__(self):
       return self.description

