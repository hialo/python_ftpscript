import ftplib
import os
import time
import sys
from ftplib import FTP

path = '/home/hialo/UnB/teste'

# TODO: Metodo para verificar a integridade do arquivo recebido. Tratamentos de excecao. Singleton para a conexao FTP?

def connect():
	#ftp = FTP('ftp2.dissect.pe')
	ftp = FTP('ftp.osuosl.org')
	try:
		#login = ftp.login ('user', 'pass')
		#print ftp.getwelcome()
		login = ftp.login()
		print 'Conexao/login efetuado com sucesso.'

		ftp.cwd ('/debian-cd/7.8.0/amd64/bt-cd')

		return ftp

	except ftplib.all_errors:
		print 'ERRO: Nao foi possivel conectar ao servidor FTP.'


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

	if newfiles:
		print "Existem " + str(len(newfiles)) + " arquivos a serem baixados."

		for i in range (0, len(newfiles)):
			downloadFile(newfiles[i], conn)

			print 'Download do arquivo ' + str(i + 1) + ' efetuado. Verificando integridade...'

			try:
				writingLogFile(newfiles[i], os.path.getsize(newfiles[i]))

			except os.error:
				print "ERRO: Nao foi possivel obter o tamanho do arquivo."
				writingLogFile(newfiles[i], 0)			

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

def verifyingIntegrity():
	print 'nothing'

#############################################################################

def main():
	ftp = connect()
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
        main()
    except KeyboardInterrupt:
        print 'Interrompido'

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
