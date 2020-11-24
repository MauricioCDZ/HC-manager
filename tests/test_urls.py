from django.urls import reverse, resolve

# Preguntas:
# 1. Documentación de las pruebas de caja blanca
# 2. ¿Solo hacer pruebas o también realizar las correcciones?

class TestUrls:

	cedula_test = {'cedula': '465789123'}

	def test_admin_url(self):
		path = reverse('app-admin')
		assert resolve(path).view_name == 'app-admin'

	def test_adminHC_url(self):
		path = reverse('app-adminHC')
		assert resolve(path).view_name == 'app-adminHC'

	def test_adminUser_url(self):
		path = reverse('app-adminUser')
		assert resolve(path).view_name == 'app-adminUser'

	def test_adminCreate_url(self):
		path = reverse('app-adminCreate')
		assert resolve(path).view_name == 'app-adminCreate'

	def test_adminEdit_url(self):
		path = reverse('app-adminEdit', kwargs=self.cedula_test)
		assert resolve(path).view_name == 'app-adminEdit'

	def test_adminLog_url(self):
		path = reverse('app-adminLog', kwargs=self.cedula_test)
		assert resolve(path).view_name == 'app-adminLog'

	def test_adminCita_url(self):
		path = reverse('app-adminCita', kwargs=self.cedula_test)
		assert resolve(path).view_name == 'app-adminCita'

	def test_adminDelHC_url(self):
		path = reverse('app-adminDelHC', kwargs=self.cedula_test)
		assert resolve(path).view_name == 'app-adminDelHC'

	def test_home_url(self):
		path = reverse('login-signIn')
		assert resolve(path).view_name == 'login-signIn'

	def test_login_url(self):
		path = reverse('login-welcome')
		assert resolve(path).view_name == 'login-welcome'

	def test_newHC_url(self):
		path = reverse('app-newHC')
		assert resolve(path).view_name == 'app-newHC'

	def test_editHC_url(self):
		path = reverse('app-editHC', kwargs=self.cedula_test)
		assert resolve(path).view_name == 'app-editHC'

	def test_logHC_url(self):
		path = reverse('app-logHC', kwargs=self.cedula_test)
		assert resolve(path).view_name == 'app-logHC'

	def test_newCita_url(self):
		path = reverse('app-newCita', kwargs=self.cedula_test)
		assert resolve(path).view_name == 'app-newCita'
	
	def test_help_url(self):
		path = reverse('app-help')
		assert resolve(path).view_name == 'app-help'