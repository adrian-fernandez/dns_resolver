#!/usr/bin/python

# -*- coding: UTF-8 -*-
# enable debugging

# Comprueba mediante varios servidores DNS la resolucion de un dominio.
# adrian.fernandez@talentocorporativo.com


import cgi
import cgitb
import sys
import os
from subprocess import Popen, PIPE
from tabulate import tabulate

####################
##		  ##
## Funciones HTML ##
##		  ##
####################

html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
}

def xstr(s):
	if s is None:
		return ''
	return str(s)

def html_escape(text):
	return "".join(html_escape_table.get(c,c) for c in text)

def html_header():
	html = "<html><head>"
	html += "</head><body>"
	return html

def html_footer():
	html = "</body></html>"
	return html

def print_title (data):
	html = "<h2>" + data + "</h2>"
	return html

def html_form(domain):
	html = "<form method='get' action='#'><label for='domain'>Dominio: </label><input type='text' name='domain' id='domain' value='" + domain + "'><input type='submit' value='Resolver'/></form>"
	return html

def home():
	html = ""
	html += html_header()
	html += html_form("")
	html += html_footer()

	return html

def html_resultado(result, domain):
	html = ""
	html += html_header()
	html += html_form(domain)
	html += "<hr><table><thead><tr><th>Servidor DNS</th><th>IP</th></tr><tbody>"

	for res in result:
		html += "<tr><td>" + (xstr(res[0])) + "</td><td>" + (xstr(res[1])) + "</td></tr>"

	html += "</tbody></table>"
	html += html_footer()

	return html


def check(domain, dns):
	process = Popen(['host', domain, dns], stdout=PIPE)
	(output, err) = process.communicate()
	exit_code = process.wait()

	for line in output.split("\n"):
		if "has address" in line:
			ip = line.split(" ")[3];
			return ip;



cgitb.enable();
print("Content-type: text/html\n\n")

form = cgi.FieldStorage() 

if "domain" in form:
	dns_list = {"156.154.70.1": "DNS Advantage", "216.146.35.35": "Dyn", "156.154.71.1": "UltraDNS", "4.2.2.1": "Verizon",  "109.69.8.51": "PuntCAT", "212.89.0.31": "TeleCable", "8.8.8.8": "Google", "195.5.64.2": "Arrakis", "208.67.222.222": "OpenDNS", "62.36.225.150": "Orange", "62.36.225.150": "Wanadoo", "8.26.56.26": "ComodoDNS"}
	results = []
	for dns in dns_list:
		results += [[dns_list[dns], check(form.getvalue('domain'), dns)]];
	print html_resultado(results, form.getvalue('domain'))

else:
	print home().encode('latin1')


