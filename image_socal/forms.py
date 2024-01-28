from django import forms
from .models import Image
from urllib import request
from django.utils.text import slugify
from django.core.files.base import ContentFile
import certifi
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

'''
В приведенном выше коде мы импортируем модули ssl и urllib.request.
Затем мы создаем объект SSLContext с желаемой версией SSL/TLS (в данном случае PROTOCOL_TLSv1_2).
Наконец, мы делаем запрос к URL-адресу, используя функцию urllib.request.urlopen, 
передавая URL-адрес и объект SSLContext.
Обратите внимание, что объект SSLContext может быть настроен с дополнительными параметрами,
такими как указание сертификата клиента или отключение проверки сертификата. 
Для получения дополнительной информации обратитесь к документации по Python.
 '''

#заменили виджет по умолчанию для url
#этот виджет формируется как input-эл-т, с атрибутом type='hidden',это делается чтобы
#поль-ль не видел поле url
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title','url','description']
        widgets = {'url':forms.HiddenInput,}

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extension = ['jpeg','jpg']
        extension = url.rsplit('.',1)[1].lower()

        if extension not in valid_extension:
            raise forms.ValidationError('Не верный url')
        return url

    def save(self,force_insert = False, force_update=False, commit=True):
        image = super(ImageForm,self).save(commit = False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        response = request.urlopen(image_url,context=context )
        image.image.save(image_name, ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image
