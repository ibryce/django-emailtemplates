from django.template.defaultfilters import striptags, linebreaksbr
from django.db import models
from csky.models import DefaultModel, SlugModel, UserModel
from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives






class ModelTemplate(SlugModel, UserModel):
  body = models.TextField() 
  def validate_context(self, context_dict):
    for required_context in self.required_contexts.all():
      if not context_dict.has_key(required_context.key):
        raise template.VariableDoesNotExist(required_context.key)
      var_type = type(context_dict[required_context.key])
      if required_context.type and not issubclass(var_type, required_context.type.model_class()):
        raise template.TemplateSyntaxError("invalid type for %s; expected %s, got %s" % (required_context.key, required_context.type.model_class(), var_type))
    return True
  def render_string(self, template_text, context_dict):
    if self.validate_context(context_dict):
      c = template.Context(context_dict)
      t = template.Template(template_text)
      return t.render(c)
    return None
  def render(self, context_dict):
    return self.render_string(self.body, context_dict)
    

class RequiredContextItem(DefaultModel, UserModel):
  template = models.ForeignKey(ModelTemplate, related_name='required_contexts')  
  key = models.SlugField(max_length=64)
  type = models.ForeignKey(ContentType, blank=True, null=True)

  def __unicode__(self):
    if self.type:
      return "%s: %s" % (self.key, self.type.model_class())
    return "%s: ANY" % (self.key,)


class EmailTemplate(ModelTemplate):
  subject = models.CharField(max_length=1024)
  txt_body = models.TextField(blank=True,null=True,help_text="If present use as the plaintext body")
  from_address = models.CharField(max_length=1024, blank=True, null=True, help_text="Specify as Full Name &lt;email@address> <br/>defaults to &lt;no-reply@SITE>")
  def visible_from_address(self):
    if self.from_address:
      return self.from_address
    site = Site.objects.get_current()
    return 'no-reply@%s' % site.domain
  def send(self, to_address, context={}, attachments=None):
    html_body = self.render(context)
    text_body = self.txt_body or striptags(html_body)
    subject = self.render_string(self.subject, context)
    if isinstance(to_address, (str,unicode)):
      to_address = (to_address,)
    msg = EmailMultiAlternatives(subject, text_body, self.visible_from_address(), to_address)
    msg.attach_alternative(html_body, "text/html")

    if attachments is not None:
        for attach in attachments:
            msg.attach(*attach)

    return msg.send()
  @staticmethod
  def send_template(slug, to_address, context={}, attachments=None):
    template = EmailTemplate.get_by_slug(slug)
    return template.send(to_address, context, attachments)

