from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@given(u'que ingreso al sistema en el dominio "{url}"')
def step_impl(context, url):
    context.driver = webdriver.Chrome()
    context.driver.get(url)
 
@given(u'escribo mi usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)

@when(u'presiono el botón Ingresar')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div[1]/div[3]/button').click()
    
@then(u'puedo ver la leyenda "{titulo}" en la pagina principal')
def step_impl(context, titulo):
    mensaje = context.driver.find_element(By.CLASS_NAME, 'titulo').text
    time.sleep(1)
    assert titulo in mensaje, mensaje
    
    
@then(u'puedo ver el mensaje "{esperado}"')
def step_impl(context, esperado):
    mensaje = context.driver.find_element(By.TAG_NAME, "strong").text
    assert esperado == mensaje, mensaje
    