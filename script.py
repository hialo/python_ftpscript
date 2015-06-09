#!/usr/bin/python

import ftplib
import os
import time
import sys, getopt
from ftplib import FTP

path = os.getenv("HOME") + "/SALTAR/ftp_files"

def connect(user, pwd):
	ftp = FTP('ftp2.dissect.pe')

	#ftp = FTP('ftp.mozilla.org')
	#login = ftp.login()
	try:
		login = ftp.login (user, pwd)

		print 'Conexao/login efetuado com sucesso.'
		print ftp.getwelcome()

		ftp.cwd ('/ftp')
		#ftp.cwd ('/pub/mozilla.org/artwork')

		return ftp

	except ftplib.all_errors:
		print 'ERRO: Nao foi possivel conectar ao servidor FTP.'
		cleanExit()


#############################################################################

def gettingFileNames():
	files = []

	for name in os.listdir(path):
		if os.path.isfile(os.path.join(path,name)):
			files.append(name)

	return files

#############################################################################

def retrievingNewFileNames(ftplist, filelist):
	newfileslist = []

	for i in range (0, len(ftplist)):
		count = 0
		for j in range (0, (len(filelist))):
			if (ftplist[i] != filelist[j]):
				count += 1

		if count == len(filelist):
			newfileslist.append (ftplist[i])

	return newfileslist

#############################################################################

def downloadFile(filename, ftp):
	rfile = open(filename, "wb")
	arg = 'RETR ' + str(filename)

	ftp.retrbinary(arg, rfile.write)

	rfile.close()

#############################################################################

def gettingNewFiles(ftplist, filelist, conn):
	newfiles = retrievingNewFileNames(ftplist, filelist)
	filename = ''

	if newfiles:
		try:
			print "Existem " + str(len(newfiles)) + " arquivos a serem baixados."

			for i in range (0, len(newfiles)):
				filename = newfiles[i]
				downloadFile(filename, conn)

				print 'Download do arquivo ' + str(i + 1) + ' efetuado. Verificando integridade...'

				if (verifyingIntegrity(filename, conn.size(filename)) == 1):
					print 'O tamanho do arquivo nao confere. Tentando novamente o download...'
					os.remove(filename)
					downloadFile(filename, conn)

				try:
					writingLogFile(newfiles[i], os.path.getsize(newfiles[i]))

				except os.error:
					print "ERRO: Nao foi possivel obter o tamanho do arquivo."
					writingLogFile(newfiles[i], 0)

		except KeyboardInterrupt:
			print 'Download do arquivo interrompido. Finalizando...'
			os.remove(filename)	

			cleanExit()

	else:
		print 'Nao existem novos arquivos a serem baixados.'

#############################################################################
# Arquivo de log criado no mesmo diretorio aonde os arquivos sao baixados (path)
#############################################################################

def writingLogFile(filename, filesize):
	log = open ('log.txt', "a")
	log.write ("Filename: " + filename + " | Size: " + str(filesize) + " bytes | Date: " + time.strftime ("%d/%m/%Y") + "\n")

	log.close()

#############################################################################

def verifyingIntegrity(filename, ftp_size):
	if (os.path.getsize(filename) == ftp_size):
		return 0
	else:
		return 1

#############################################################################

def cleanExit():
	try:
		sys.exit(0)
	except SystemExit:
		os._exit(0)	

#############################################################################	

def main(argv):
	user = ''
	pwd  = ''
	
	try:
		myopts, args = getopt.getopt(argv, "u:p:")
	except getopt.GetoptError:
		print "Usage: script.py -u USER -p PASSWORD"
		cleanExit()

	for opt, arg in myopts:
		if opt == '-u':
			user = arg
		elif opt == '-p':
			pwd = arg

	ftp = connect(user, pwd)
	currdir = os.getcwd()

	os.chdir(path)

	ftpfilelist = ftp.nlst()
	dirfilelist = gettingFileNames()

	gettingNewFiles(ftpfilelist, dirfilelist, ftp)

	os.chdir(currdir)

	ftp.quit()

#############################################################################

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Interrompido.'

        cleanExit()
		