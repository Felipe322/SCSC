from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys


@given(u'que ingreso al sistema en el dominio "{url}"')
def step_impl(context, url):
    context.driver = webdriver.Firefox()
    context.driver.get(url)

@given(u'escribo mi usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)

@when(u'presiono el boton ingresar')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div[1]/div[3]/button').click()


@when(u'seleciono la pestaña "Administración de areas"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/aside/div[2]/div[2]/ul/li[4]/a').click()

@when(u'seleciono la opcion "Agregar area"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/aside/div[2]/div[2]/ul/li[4]/div/div/ul/li[2]/a').click()

@when(u'ingreso el nombre de un area "{nombre}" y sus siglas "{siglas}"')
def step_impl(context, nombre, siglas):
    context.driver.find_element(By.ID, 'id_nombre').send_keys(nombre)
    context.driver.find_element(By.ID, 'id_siglas').send_keys(siglas + Keys.ENTER)


@when(u'selecciono el boton "Agregar"')
def step_impl(context):
    pass
    # context.driver.find_element(By.LINK_TEXT, 'Agregar').click()


