# ddah-promises

[![Build Status](https://travis-ci.org/ciudadanointeligente/ddah-promises.png?branch=master)](https://travis-ci.org/ciudadanointeligente/ddah-promises)

Django's promises egg.

## Quick start

1.-  Add "ddah-promises" to INSTALLED_APPS:

>  **INSTALLED_APPS** = {
    ...
    'ddah-promises'
  }

2.-  Include the ddah-promises URLconf in urls.py:

>  url(r'^ddah-promises/', include('ddah-promises.urls'))

3.-  Run `python manage.py syncdb` to create ddah-promises's models.

This project is licensed under the GNU Affero General Public License (AGPL). For more information you can access to the [digital license edition here](http://www.gnu.org/licenses/agpl-3.0.html).

### Everything else:

For more information about us, our site [Fundación Ciudadano Inteligente](http://www.ciudadanointeligente.org/).
And if you want help with patches, report bugs or replicate our project check [our repositories](https://github.com/ciudadanointeligente/).
