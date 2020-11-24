from django.test import RequestFactory, TestCase
from django.urls import reverse
import hc_manager.views as views


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
        self.user_new = {'nombre':'test', 'edad':'15', 'direccion':'test', 'sexo':'masculino', 'cedula':'111111', 'ips' : ''}
        self.user_new_ips = {'nombre':'test_ips', 'edad':'15', 'direccion':'test', 'sexo':'masculino', 'cedula':'222222', 'ips' : 'test_ips'}
        self.cita_new = {'peso':'69','estatura':'170','actividad':'frecuente','dieta':'papa','enfermedades':'no','valoracion':'positivo','motivo':'test','comentario':'test'}

    def test_post_ips_newHC(self):
        request = self.factory.post('newHC/', self.user_new_ips)
        response = views.newHC(request)
        assert response.status_code == 200

    def test_post_newHC(self):
        request = self.factory.post('newHC/', self.user_new)
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