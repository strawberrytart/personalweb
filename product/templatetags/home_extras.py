from django import template

register = template.Library()

@register.simple_tag
def relative_url(value, field_name, urlencode=None): #( <page number>, <string 'page'>, <part of the url that is the query, default to None>)

    url = '?{}={}'.format(field_name, value) # '?{page}={page number}'

    if urlencode:
        querystring = urlencode.split('&') 
        
        # split url by ampersand 
        # page=2&category=Pumps&brand=SPECK
        # querystring = ['page=2', 'category=Pump', 'brand=SPECK']

        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)

        #filtered_querystring = ['category=Pump', 'brand=SPECK']

        encoded_querystring = '&'.join(filtered_querystring)

        # encoded_querystring = 'category=Pump&brand=SPECK'


        url = '{}&{}'.format(url, encoded_querystring)

        # url = '{page=2}&{category=Pump&brand=SPECK}'

    return url