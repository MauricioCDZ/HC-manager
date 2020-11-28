from django.test import RequestFactory, TestCase
from django.urls import reverse
import hc_manager.views as views
import login.views as lviews


class TestViews(TestCase):

    def setUp(self):
        # Every test needs access to the request factory
        self.factory = RequestFactory()
        self.user_legit = {'nombre':'naruto', 'edad':'12', 'direccion':'12001 Chalon Rd', 'sexo':'masculino', 'cedula':'465789123', 'ips' : [ 'ips', 'coopetran' ], 'creacion' : '29-05-2020-07:34:52', "modificacion" : "20-11-2020-22:38:55", "cambios" : {
    "09-11-2020-00:08:50" : {
      "fecha" : "09-11-2020-00:08:50",
      "valores" : [ [ "edad", "13" ], [ "sexo", "masculino" ], [ "modificacion", "09-11-2020-00:08:50" ] ]
    },
    "20-11-2020-22:38:55" : {
      "fecha" : "20-11-2020-22:38:55",
      "valores" : [ [ "edad", "12" ], [ "sexo", "masculino" ], [ "modificacion", "20-11-2020-22:38:55" ] ]
    },
    "29-05-2020-01:07:35" : {
      "fecha" : "29-05-2020-01:07:35",
      "valores" : [ [ "nombre", "Sancho Panza" ], [ "edad", "32" ], [ "direccion", "Un lugar de la mancha" ], [ "sexo" ], [ "cedula", "465789123" ], [ "ips" ], [ "creacion", "29-05-2020-01:07:35" ], [ "modificacion", "29-05-2020-01:07:35" ], [ "citas" ], "" ]
    },
    "29-05-2020-07:34:52" : {
      "fecha" : "29-05-2020-07:34:52",
      "valores" : [ [ "nombre", "naruto" ], [ "edad", "12" ], [ "direccion", "12001 Chalon Rd" ], [ "sexo" ], [ "cedula", "465789123" ], [ "ips", [ "ips", "coopetran" ] ], [ "creacion", "29-05-2020-07:34:52" ], [ "modificacion", "29-05-2020-07:34:52" ], [ "citas" ], "" ]
    }}}
        self.user_new = {'nombre':'test_ips', 'edad':'15', 'direccion':'test', 'sexo':'masculino', 'cedula':'222222', 'ips' : 'test_ips'}
        self.cita_new = {'peso':'69','estatura':'170','actividad':'frecuente','dieta':'papa','enfermedades':'no','valoracion':'positivo','motivo':'test','comentario':'test'}

    def test_post_ips_newHC(self):
        request = self.factory.post('newHC/', self.user_new)
        response = views.newHC(request)
        assert response.status_code == 200

    def test_post_newHC(self):
        user = self.user_new
        user['ips'] = ''
        request = self.factory.post('newHC/', user)
        response = views.newHC(request)
        assert response.status_code == 200

    def test_get_newHC(self):
        path = reverse('app-newHC')
        request = self.factory.get(path)
        response = views.newHC(request)
        assert response.status_code == 200

    def test_get_editHC(self):
        path = reverse('app-editHC', kwargs={'cedula': '465789123'})
        request = self.factory.get(path)
        response = views.editHC(request, cedula='465789123')
        assert 'editHC/465789123/' in str(response.content)

    def test_post_ips_editHC(self):
        request = self.factory.post('/editHC/465789123', self.user_legit)
        response = views.editHC(request, cedula='465789123')
        assert response.status_code == 200

    def test_post_editHC(self):
        user = self.user_legit
        user['ips'] = ''
        request = self.factory.post('/editHC/465789123', user)
        response = views.editHC(request, cedula='465789123')
        assert response.status_code == 200

    def test_get_logHC(self):
        path = reverse('app-logHC', kwargs={'cedula': '465789123'})
        request = self.factory.get(path)
        response = views.logHC(request, cedula='465789123')
        assert response.status_code == 200

    def test_post_newCita(self):
        request = self.factory.post('/newCita/465789123', self.cita_new)
        response = views.newCita(request, cedula='465789123')
        assert response.status_code == 200

    def test_get_newCita(self):
        path = reverse('app-newCita', kwargs={'cedula': '465789123'})
        request = self.factory.get(path)
        response = views.newCita(request, cedula='465789123')
        assert response.status_code == 200

    def test_post_search_adminHC(self):
        request = self.factory.post('/adminHC/', {'cedula_search':'465789123'})
        response = views.adminHC(request)
        assert response.status_code == 200

    def test_post_login_adminHC(self):
        request = self.factory.post('/adminHC/', {'email':'admin@jmail.com', 'pass':'test123'})
        response = views.adminHC(request)
        assert response.status_code == 200

    def test_admin(self):
        path = reverse('app-admin')
        request = self.factory.get(path)
        response = views.admin(request)
        assert response.status_code == 200

    def test_get_adminUser(self):
        path = reverse('app-adminUser')
        request = self.factory.get(path)
        response = views.adminUser(request)
        assert response.status_code == 200

    def test_post_adminUser(self):
        request = self.factory.post('/adminUser/', {'email':'admin2@jmail.com', 'pass':'test123'})
        response = views.adminUser(request)
        assert response.status_code == 200

    def test_post_ips_adminCreate(self):
        request = self.factory.post('/adminCreate/', self.user_new)
        response = views.adminCreate(request)
        assert response.status_code == 200

    def test_post_no_ips_adminCreate(self):
        user = self.user_new
        user['ips'] = ''
        request = self.factory.post('/adminCreate/', user)
        response = views.adminCreate(request)
        assert response.status_code == 200

    def test_get_adminCreate(self):
        path = reverse('app-adminCreate')
        request = self.factory.get(path)
        response = views.adminCreate(request)
        assert response.status_code == 200

    def test_post_ips_adminEdit(self):
        request = self.factory.post('/adminEdit/465789123', self.user_legit)
        response = views.adminEdit(request, cedula='465789123')
        assert response.status_code == 200

    def test_post_no_ips_adminEdit(self):
        user = self.user_legit
        user['ips'] = ''
        request = self.factory.post('/adminEdit/465789123', user)
        response = views.adminEdit(request, cedula='465789123')
        assert response.status_code == 200

    def test_get_adminEdit(self):
        path = reverse('app-adminEdit', kwargs={'cedula': '465789123'})
        request = self.factory.get(path)
        response = views.adminEdit(request, cedula='465789123')
        assert response.status_code == 200

    def test_get_adminLog(self):
        path = reverse('app-adminLog', kwargs={'cedula': '465789123'})
        request = self.factory.get(path)
        response = views.adminLog(request, cedula='465789123')
        assert response.status_code == 200

    def test_post_adminCita(self):
        request = self.factory.post('/adminCita/465789123', self.cita_new)
        response = views.adminCita(request, cedula='465789123')
        assert response.status_code == 200

    def test_get_adminCita(self):
        path = reverse('app-adminCita', kwargs={'cedula': '465789123'})
        request = self.factory.get(path)
        response = views.adminCita(request, cedula='465789123')
        assert response.status_code == 200

    def test_get_adminDelHC(self):
        path = reverse('app-adminDelHC', kwargs={'cedula': '222222'})
        request = self.factory.get(path)
        response = views.adminDelHC(request, cedula='222222')
        assert response.status_code == 200

    def test_get_help(self):
        path = reverse('app-help')
        request = self.factory.get(path)
        response = views.help(request)
        assert response.status_code == 200

    def test_get_signIn(self):
        path = reverse('login-signIn')
        request = self.factory.get(path)
        response = lviews.signIn(request)
        assert response.status_code == 200

    def test_post_search_postSign(self):
        request = self.factory.post('/postSign/', {'email':'gargal@gmail.com', 'pass':'test123'})
        response = lviews.postSign(request)
        assert response.status_code == 200

    def test_post_login_postSign(self):
        request = self.factory.post('/postSign/', {'cedula_search':'465789123'})
        response = lviews.postSign(request)
        assert response.status_code == 200

    def test_get_postSign(self):
        path = reverse('login-welcome')
        request = self.factory.get(path)
        response = lviews.postSign(request)
        assert response.status_code == 200
